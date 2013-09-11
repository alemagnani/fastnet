#!/bin/sh

python ~/fastnet/fastnet/trainer.py  \
  --data_dir /ssd/nn-data/imagenet/ \
  --param_file config/imagenet.cfg \
  --data_provider imagenet \
  --train_range 0-1200 \
  --test_range 1200-1300 \
  --save_freq 100 \
  --test_freq 100 \
  --adjust_freq 100 \
  --learning_rate "[0.1, 0.1]" \
  --batch_size 128 \
  --checkpoint_dir ~/fastnet/fastnet/checkpoint/ \
  --trainer catewise \
  --num_batch "[100, 30000]" \
  --num_caterange_list "[100, 1000]" \
  $@
