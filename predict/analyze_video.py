"""
analyzes a video using DeepPoseKit
give command line arguments: video, model_name, skelton (all with full paths)
"""
from deepposekit.io import DataGenerator, VideoReader, VideoWriter
from deepposekit.io import VideoReader, VideoWriter, utils
from deepposekit.models import load_model
from utils import analyze_video, make_tracking_video
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm
import cv2
import sys
import os



# parse args
video, model_name, skeleton = sys.argv[1:]

# # predict
# model = load_model(model_name)
# reader = VideoReader(video, batch_size=32, gray=True, frame_size=model.input_shape)
# predictions = model.predict(reader, verbose=1, workers=1, use_multiprocessing=False)
# reader.close()
#
# # get column names
# features = list(pd.read_csv(skeleton).name)
# columns = []
# for f in features:
#     columns += [f+'_x', f+'_y', f+'_confidence']
#
# # save to csv
# data = pd.DataFrame(columns=columns, index=np.arange(predictions.shape[0]))
# data[:] = np.reshape(predictions, (predictions.shape[0], -1))
# data.to_csv(os.path.splitext(video)[0] + '_tracking.csv')

model = load_model(model_name)
predictions = analyze_video(video, model, skeleton)
make_tracking_video(video, skeleton, predictions=predictions)  # add back predictions
