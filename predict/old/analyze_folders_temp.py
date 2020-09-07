"""
analyzes multiple videos using DeepPoseKit
given 'stim' or 'tank' as command line argument, analyzes all videos for stim or tank experiments
can optionally specify specific sessions to analyze as additional command line arguments
"""

# todo: option for overwriting files // make sure works with tank directory structure as well

from deepposekit.io import DataGenerator, VideoReader, VideoReaderTest, VideoWriter
# from predict.utils import analyze_video, make_tracking_video
# from deepposekit.models import load_model
import pandas as pd
import numpy as np
import yaml
import glob
import sys
import os
import cv2

import time
# os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


# parse input arguments
vid_type = sys.argv[1]  # 'stim' or 'tank'
with open('config.yaml', 'r') as file:
	cfg = yaml.safe_load(file)[vid_type]

# find video folders
if len(sys.argv)>2:
	vid_folders = sys.argv[2:]
else:
	vid_folders = [f.path for f in os.scandir(cfg['data_dir']) if f.is_dir()]

# load model
# model = load_model(cfg['model'])

# # analyze videos
# for vid_folder in vid_folders:
# 	vids = glob.glob(os.path.join(vid_folder, '*.avi'))
# 	vids = [vid for vid in vids if 'concatenated' not in vid and 'tracking' not in vid]  # don't add concatenated vids
    
# 	for idx, vid in enumerate(vids):
# 		print('\n({}/{})--------- analyzing {}'.format(idx, len(vids), vid))
		
# 		# analyze video
# 		# reader = cv2.VideoCapture(vid)
# 		time.sleep(1)
# 		print('outer 1')
# 		reader = VideoReaderTest(vid);
# 		reader.close()
# 		print('outer 2')
# 		# time.sleep(.01)
# 		# predictions = model.predict(reader, verbose=1)
# 		# reader.release()
# 		# while reader.isOpened():
# 		# 	pass
# 		# del reader
# 		# time.sleep(.01)


for i in range(500):
	print(i)
	# time.sleep(.1)
	reader = VideoReaderTest(r'Z:\locker\ShareData\chin_for_rick\191206_C1stim_wNS\20191206_3.avi');
	# reader = VideoReaderTest(r'Z:\locker\ShareData\chin_for_rick\191206_C1stim_wNS\20191206_4.avi');
	reader.close()
	del reader
	time.sleep(.1)



print('yes')

