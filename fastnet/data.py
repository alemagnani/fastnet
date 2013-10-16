from PIL import Image
from pycuda import gpuarray, driver
from fastnet.cuda_kernel import gpu_partial_copy_to
from os.path import basename
from fastnet import util
import Queue
import cPickle
import collections
import glob
import numpy as np
import os
import random
import re
import sys
import threading
import time

def copy_to_gpu(data):
  return gpuarray.to_gpu(data.astype(np.float32))


class BatchData(object):
  def __init__(self, data, labels, epoch):
    self.data = data
    self.labels = labels
    self.epoch = epoch


class DataProvider(object):
  def __init__(self, data_dir='.', batch_range=None, test = False):
    self.data_dir = data_dir
    self.meta_file = os.path.join(data_dir, 'batches.meta')

    self.curr_batch_index = 0
    self.curr_batch = None
    self.curr_epoch = 1

    if os.path.exists(self.meta_file):
      self.batch_meta = util.load(self.meta_file)
    else:
      util.log_warn('Missing metadata for loader.')

    if batch_range is None:
      self.batch_range = self.get_batch_indexes()
    else:
      self.batch_range = batch_range
    random.shuffle(self.batch_range)

    self.index = 0

  def reset(self):
    self.curr_batch_index = 0
    self.curr_batch = None
    self.curr_epoch = 1
    random.shuffle(self.batch_range)

  def get_next_index(self):
    self.curr_batch_index = self.curr_batch_index + 1
    if self.curr_batch_index == len(self.batch_range) + 1:
      random.shuffle(self.batch_range)
      self.curr_epoch += 1
      self.curr_batch_index = 1

      self._handle_new_epoch()


    self.curr_batch = self.batch_range[self.curr_batch_index - 1]

  def _handle_new_epoch(self):
    '''
    Called when a new epoch starts.
    '''
    pass

  def get_batch_num(self):
    return len(self.batch_range)

  @property
  def image_shape(self):
    return (3, self.inner_size, self.inner_size)

  @property
  def data_dim(self):
    return self.inner_size ** 2 * 3


def _prepare_images(data_dir, category_range, batch_range, batch_meta):
  assert os.path.exists(data_dir), data_dir

  dirs = glob.glob(data_dir + '/n*')
  synid_to_dir = {}
  for d in dirs:
    synid_to_dir[basename(d)[1:]] = d

  if category_range is None:
    cat_dirs = dirs
  else:
    cat_dirs = []
    for i in category_range:
      synid = batch_meta['label_to_synid'][i]
      # util.log('Using category: %d, synid: %s, label: %s', i, synid, self.batch_meta['label_names'][i])
      cat_dirs.append(synid_to_dir[synid])

  images = []
  batch_dict = dict((k, k) for k in batch_range)

  for d in cat_dirs:
    imgs = [v for i, v in enumerate(glob.glob(d + '/*.jpg')) if i in batch_dict]
    images.extend(imgs)


  return np.array(images)


class ImageNetDataProvider(DataProvider):
  img_size = 256
  border_size = 16
  inner_size = 224

  def __init__(self, data_dir, batch_range=None, test = False, category_range=None, batch_size=1024):
    DataProvider.__init__(self, data_dir, batch_range, test)
    self.batch_size = batch_size
    self.test = test
    self.multiview = test
    self.images = _prepare_images(data_dir, category_range, batch_range, self.batch_meta)
    self.num_view = 5 * 2

    assert len(self.images) > 0

    self._shuffle_batches()

    if 'data_mean' in self.batch_meta:
      data_mean = self.batch_meta['data_mean']
    else:
      data_mean = util.load(data_dir + 'image-mean.pickle')['data']

    self.data_mean = (data_mean
        .astype(np.single)
        .T
        .reshape((3, 256, 256))[:,
                                self.border_size:self.border_size + self.inner_size,
                                self.border_size:self.border_size + self.inner_size]
        .reshape((self.data_dim, 1)))
    util.log('Starting data provider with %d batches', len(self.batches))

  def _shuffle_batches(self):
    # build index vector into 'images' and split into groups of batch-size
    image_index = np.arange(len(self.images))
    np.random.shuffle(image_index)

    self.batches = np.array_split(image_index,
                                  util.divup(len(self.images), self.batch_size))

    self.batch_range = range(len(self.batches))
    np.random.shuffle(self.batch_range)

  def _handle_new_epoch(self):
    self._shuffle_batches(self.batch_size)

  def __trim_borders(self, images, target):
    if self.test:
      start_positions = [(0, 0), (0, self.border_size * 2), (self.border_size, self.border_size),
                          (self.border_size *2 , 0), (self.border_size * 2 , self.border_size * 2)]
      end_positions = [(x + self.inner_size, y + self.inner_size) for (x, y) in start_positions]
      for i in xrange(self.num_view / 2):
        startY , startX = start_positions[i][0], start_positions[i][1]
        endY, endX = end_positions[i][0], end_positions[i][1]
        num_image = len(images)
        pic = np.array([img[:, startY:endY, startX:endX]  for img in images])
        target[:, i * num_image: (i + 1) * num_image] = pic.reshape((self.data_dim, num_image))
        target[:, (self.num_view/2 +i) * num_image:(self.num_view/2 +i+1)* num_image] = pic[:, :, ::-1, :].reshape((self.data_dim, num_image))
    else:
      for idx, img in enumerate(images):
        startY, startX = np.random.randint(0, self.border_size * 2 + 1), np.random.randint(0, self.border_size * 2 + 1)
        endY, endX = startY + self.inner_size, startX + self.inner_size
        pic = img[:, startY:endY, startX:endX]
        if np.random.randint(2) == 0:  # also flip the image with 50% probability
          pic = pic[:, :, ::-1]
        target[:, idx] = pic.reshape((self.data_dim,))

  def get_next_batch(self):
    self.get_next_index()

    epoch = self.curr_epoch
    batchnum = self.curr_batch
    names = self.images[self.batches[batchnum]]
    num_imgs = len(names)
    labels = np.zeros((1, num_imgs))
    if self.test:
        cropped = np.ndarray((self.data_dim, num_imgs * self.num_view), dtype=np.uint8)
    else:
        cropped = np.ndarray((self.data_dim, num_imgs), dtype = np.uint8)
    # _load in parallel for training
    st = time.time()
    images = []
    for idx, filename in enumerate(names):
#       util.log('Loading... %s %s', idx, filename)
      jpeg = Image.open(filename)
      if jpeg.mode != "RGB": jpeg = jpeg.convert("RGB")
      # starts as rows * cols * rgb, tranpose to rgb * rows * cols
      img = np.asarray(jpeg, np.uint8).transpose(2, 0, 1)
      images.append(img)

    self.__trim_borders(images, cropped)

    load_time = time.time() - st

    clabel = []
    # extract label from the filename
    for idx, filename in enumerate(names):
      filename = os.path.basename(filename)
      synid = filename[1:].split('_')[0]
      label = self.batch_meta['synid_to_label'][synid]
      labels[0, idx] = label

    st = time.time()
    cropped = cropped.astype(np.single)
    cropped = np.require(cropped, dtype=np.single, requirements='C')
    cropped -= self.data_mean

    align_time = time.time() - st

    labels = np.array(labels)
    labels = labels.reshape(labels.size,)
    labels = np.require(labels, dtype=np.single, requirements='C')

    # util.log("Loaded %d images in %.2f seconds (%.2f _load, %.2f align)",
    #         num_imgs, time.time() - start, load_time, align_time)
    # self.data = {'data' : SharedArray(cropped), 'labels' : SharedArray(labels)}

    return BatchData(cropped, labels, epoch)


class CifarDataProvider(DataProvider):
  img_size = 32
  border_size = 0
  inner_size = 32

  BATCH_REGEX = re.compile('^data_batch_(\d+)$')
  def get_next_batch(self):
    self.get_next_index()
    filename = os.path.join(self.data_dir, 'data_batch_%d' % self.curr_batch)

    data = util.load(filename)
    img = data['data'] - self.batch_meta['data_mean']
    return BatchData(np.require(img, requirements='C', dtype=np.float32),
                     np.array(data['labels']),
                     self.curr_epoch)

  def get_batch_indexes(self):
    names = self.get_batch_filenames()
    return sorted(list(set(int(DataProvider.BATCH_REGEX.match(n).group(1)) for n in names)))


class IntermediateDataProvider(DataProvider):
  def __init__(self, data_dir, batch_range, data_name):
    DataProvider.__init__(self, data_dir, batch_range)
    self.data_name = data_name

  def get_next_batch(self):
    self.get_next_index()

    filename = os.path.join(self.data_dir + '.%s' % self.curr_batch)
    util.log('reading from %s', filename)

    data_dic = util.load(filename)
    data  = data_dic[self.data_name].transpose()
    labels = data_dic['labels']
    data = np.require(data, requirements='C', dtype=np.float32)
    return BatchData(data, labels, self.curr_epoch)



class MemoryDataProvider(DataProvider):
  def __init__(self, data_holder, batch_range = None, data_name = 'fc'):
    data_holder.finish_push()
    if batch_range is None:
      batch_range  = range(data_holder.get_count())

    DataProvider.__init__(self, data_dir = '.', batch_range = batch_range)
    self.data_holder = data_holder
    self.data_list = self.data_holder.memory_chunk
    self.data_name = data_name

  def get_next_batch(self):
    self.get_next_index()

    data = self.data_list[self.curr_batch]
    labels = data['labels']
    img = np.require(data[self.data_name].transpose(), requirements='C', dtype=np.float32)
    return BatchData(img, labels, self.curr_epoch)


class ReaderThread(threading.Thread):
  def __init__(self, queue, dp):
    threading.Thread.__init__(self)
    self.daemon = True
    self.queue = queue
    self.dp = dp
    self._stop = False
    self._running = True

  def run(self):
    while not self._stop:
      #util.log('Fetching...')
      self.queue.put(self.dp.get_next_batch())
      #util.log('%s', self.dp.curr_batch_index)
      #util.log('Done.')

    self._running = False

  def stop(self):
    self._stop = True
    while self._running:
      _ = self.queue.get(0.1)


class ParallelDataProvider(DataProvider):
  def __init__(self, dp):
    self.dp = dp
    self._reader = None
    self.reset()

  def _start_read(self):
    util.log('Starting reader...')
    assert self._reader is None
    self._reader = ReaderThread(self._data_queue, self.dp)
    self._reader.start()

  @property
  def image_shape(self):
    return self.dp.image_shape

  @property
  def multiview(self):
    if hasattr(self.dp, 'multiview'):
      return self.dp.multiview
    else:
      return False

  @property
  def num_view(self):
    if hasattr(self.dp, 'num_view'):
      return self.dp.num_view
    else:
      assert 'Doesn\'t have num_view attr'

  def reset(self):
    self.dp.reset()

    if self._reader is not None:
      self._reader.stop()

    self._reader = None
    self._data_queue = Queue.Queue(1)
    self._gpu_batch = None
    self.index = 0

  def _fill_reserved_data(self):
    batch_data = self._data_queue.get()

    #timer = util.EZTimer('fill reserved data')

    self.curr_epoch = batch_data.epoch
    batch_data.data = copy_to_gpu(batch_data.data)
    batch_data.labels = copy_to_gpu(batch_data.labels)
    self._gpu_batch = batch_data

  def get_next_batch(self, batch_size, num_view = 1):
    if self._reader is None:
      self._start_read()

    if self._gpu_batch is None:
      self._fill_reserved_data()

    height, width = self._gpu_batch.data.shape
    gpu_data = self._gpu_batch.data
    gpu_labels = self._gpu_batch.labels

    if self.index + batch_size >=  width:
      width = width - self.index
      labels = gpu_labels[self.index/num_view:(self.index + batch_size) / num_view]

      data = gpuarray.zeros((height, width), dtype = np.float32)
      gpu_partial_copy_to(gpu_data, data, 0, height, self.index, self.index + width)

      self.index = 0
      self._fill_reserved_data()
    else:
      labels = gpu_labels[self.index/ num_view:(self.index + batch_size) / num_view]
      data = gpuarray.zeros((height, batch_size), dtype = np.float32)
      gpu_partial_copy_to(gpu_data, data, 0, height, self.index, self.index + batch_size)
      self.index += batch_size
    return BatchData(data, labels, self._gpu_batch.epoch)


dp_dict = {}
def register_data_provider(name, _class):
  if name in dp_dict:
    print 'Data Provider', name, 'already registered'
  else:
    dp_dict[name] = _class

def get_by_name(name):
  if name not in dp_dict:
    print >> sys.stderr, 'There is no such data provider --', name, '--'
    sys.exit(-1)
  else:
    dp_klass = dp_dict[name]
    def construct_dp(*args, **kw):
      dp = dp_klass(*args, **kw)
      return ParallelDataProvider(dp)
    return construct_dp


register_data_provider('cifar10', CifarDataProvider)
register_data_provider('imagenet', ImageNetDataProvider)
register_data_provider('intermediate', IntermediateDataProvider)
register_data_provider('memory', MemoryDataProvider)
