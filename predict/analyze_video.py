"""
analyzes a video using DeepPoseKit
give command line arguments: video, model_name, skelton (all with full paths)
"""


import sys
import numpy as np
from deepposekit.models import load_model
from deepposekit.io import DataGenerator, VideoReader, VideoWriter
import pandas as pd
import os

# parse input arguments
video, model_name, skeleton = sys.argv[1:]

# for debugging
# video = r'Z:\locker\ShareData\chin_for_rick\191206_C1stim_wNS\20191206_0.avi'
# model_name = r'D:\github\fish-tracking\train\models\stim_model_1.h5'
# skeleton = r'D:\github\fish-tracking\label\skeletons\stim_skeleton.csv'

# settings
batch_size = 64
max_frames = None # set to None unless debugging

# load model and video
model = load_model(model_name)
reader = VideoReader(video, batch_size=batch_size, gray=True, frame_size=model.input_shape)

# predict
max_batches = max_frames//batch_size if max_frames else None
predictions = model.predict(reader, verbose=1, steps=max_batches)
reader.close()

# get column names
features = list(pd.read_csv(skeleton).name)
columns = []
for f in features:
	columns += [f+'_x', f+'_y', f+'_confidence']

# save data
data = pd.DataFrame(columns=columns, index=np.arange(predictions.shape[0]))
data[:] = np.reshape(predictions, (predictions.shape[0], -1))
data.to_csv(os.path.splitext(video)[0] + '_tracking.csv')