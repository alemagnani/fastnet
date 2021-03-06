#!/usr/bin/python2.7
'''
This test is for naive trainer to traine a full imagenet model
'''

from fastnet import data, trainer, net, parser

test_id = 'multiview'

data_dir = '/ssd/nn-data/imagenet/'
checkpoint_dir = '/home/justin/fastnet/fastnet/checkpoint/'
param_file = '/home/justin/fastnet/config/imagenet.cfg'
output_dir = ''
output_method = 'disk'

train_range = range(101, 102) #1,2,3,....,40
test_range = range(1, 2) #41, 42, ..., 48
data_provider = 'imagenet'


multiview = True

train_dp = data.get_by_name(data_provider)(data_dir,train_range)
test_dp = data.get_by_name(data_provider)(data_dir, test_range, multiview = True)
checkpoint_dumper = trainer.CheckpointDumper(checkpoint_dir, test_id)

model = checkpoint_dumper.get_checkpoint()
if model is None:
  model = parser.parse_config_file(param_file)

save_freq = 100
test_freq = 4
adjust_freq = 100
factor = 1
num_epoch = 50
learning_rate = 0.1
batch_size = 128
image_color = 3
image_size = 224
image_shape = (image_color, image_size, image_size, batch_size)
net = parser.load_model(net.FastNet(image_shape), model)

param_dict = globals()
t = trainer.Trainer(**param_dict)
t.train(num_epoch)
