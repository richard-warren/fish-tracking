"""
makes video showing DeepPoseKit tracking
give command line arguments: video, skelton (all with full paths)
"""

from deepposekit.io import VideoReader, VideoWriter, utils
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm
import sys
import cv2
import os
import ipdb

# parse input arguments
video, skeleton_name = sys.argv[1:]
fps = 300

# inits
video_output = os.path.splitext(video)[0] + '_tracking.avi'
predictions = pd.read_csv(os.path.splitext(video)[0] + '_tracking.csv').to_numpy()[:,1:]
predictions = predictions.reshape((-1, int(predictions.shape[1]/3), 3))  # (frane_num X feature_num X (x,y,confidence))
skeleton = utils.initialize_skeleton(skeleton_name)
graph = skeleton[["tree", "swap_index"]].values[:,0]
cmap = plt.cm.hsv(np.linspace(0, 1, len(graph)))[:, :3][:, ::-1] * 255

# make video
reader = VideoReader(video, batch_size=1)
writer = VideoWriter(video_output, reader[0].shape[1:3], 'MP4V', fps)

for frame_num, frame, keypoints in tqdm.tqdm(zip(range(len(reader)), reader, predictions)):
    frame = frame[0].copy()
    
    # lines
    for idx, node in enumerate(graph):
        if node >= 0:
            pt1 = keypoints[idx]
            pt2 = keypoints[node]
            cv2.line(frame, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (0, 0, 255), 1, cv2.LINE_AA)
    # dots
    for idx, keypoint in enumerate(keypoints):
        keypoint = keypoint.astype(int)
        cv2.circle(frame, (keypoint[0], keypoint[1]), 2, tuple(cmap[idx]), -1, lineType=cv2.LINE_AA)
    # frame number
    frame = cv2.putText(frame, f'frame {frame_num}', (0,round(frame.shape[0]*.95)), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))
    
    writer.write(frame)

writer.close()
reader.close()
