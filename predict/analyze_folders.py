"""
analyzes multiple videos using DeepPoseKit
given 'stim' or 'tank' as command line argument, analyzes all videos for stim or tank experiments
-overwrite flag overwrites existing tracking files
"""


from deepposekit.io import DataGenerator, VideoReader, VideoWriter
from predict.utils import analyze_video, make_tracking_video
from deepposekit.models import load_model
import pandas as pd
import numpy as np
import argparse
import yaml
import glob
import sys
import os
import tensorflow as tf


# parse input arguments
parser = argparse.ArgumentParser()
parser.add_argument('vid_type', help="'stim' or 'tank'")
parser.add_argument('-overwrite', help="overwrite existing files", action='store_true')
args = parser.parse_args()
vid_type = args.vid_type

# load config
with open('config.yaml', 'r') as file:
	cfg = yaml.safe_load(file)[vid_type]

# find video folders
vid_folders = [f.path for f in os.scandir(cfg['data_dir']) if f.is_dir()]

# load model
model = load_model(cfg['model'])

# analyze videos
for vid_folder in vid_folders:
	vids = glob.glob(os.path.join(vid_folder, '*.avi'))
	vids = [vid for vid in vids if 'concatenated' not in vid and 'tracking' not in vid]  # don't add concatenated vids
	vids.sort()

	for idx, vid in enumerate(vids):
		if args.overwrite or not os.path.exists(os.path.splitext(vid)[0] + '_tracking.csv'):
			print('\n({}/{})--------- analyzing {}'.format(idx, len(vids), vid))
			predictions = analyze_video(vid, model, cfg['skeleton'])
			make_tracking_video(vid, cfg['skeleton'], predictions=predictions)
			# tf.keras.backend.clear_session() # temp



