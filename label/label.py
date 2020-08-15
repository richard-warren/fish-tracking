import sys
import numpy as np
import cv2
import h5py
import matplotlib.pyplot as plt
from deepposekit.io import VideoReader, DataGenerator, initialize_dataset
from deepposekit.annotate import KMeansSampler
import tqdm
import glob
import pandas as pd
from os.path import expanduser
import os



## sample random frames from video

# settings
video = r'Z:\locker\ShareData\Chin_for_Rick\200527_c1stim_wNS\20200527_42.avi'
n_frames = 40  # frames to include in training set

reader = VideoReader(video, gray=True, batch_size=1)
n_sample_frames = len(reader)  # training set frames are selected from random sample of n_sample_frames
random_frames = []
for idx in np.sort(np.random.choice(range(len(reader)), n_sample_frames)):
    random_frames.append(reader[idx][...,0])
reader.close()
random_frames = np.concatenate(random_frames)

## k-means clustering

# settings
n_clusters = 10

kmeans = KMeansSampler(n_clusters=n_clusters, max_iter=1000, n_init=10, batch_size=100, verbose=True)
kmeans.fit(random_frames)
kmeans.plot_centers(n_rows=2)
kmeans_sampled_frames, kmeans_cluster_labels = kmeans.sample_data(
    random_frames, n_samples_per_label=np.ceil(n_frames/n_clusters).astype('int'))

##