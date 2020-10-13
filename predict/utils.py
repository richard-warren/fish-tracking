from deepposekit.io import DataGenerator, VideoReader, VideoWriter
from deepposekit.io import VideoReader, VideoWriter, utils
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
import tqdm
import cv2
import os
os.environ['TF_FORCE_GPU_ALLOW_GROWTH'] = 'true'


def analyze_video(video, model, skeleton_name, batch_size=16):
	"""
	analyze a video and save results to 'video_tracking.csv' in same directory
	video: 	  		 full path to video
	model:	  	  	 deepposekit model instance
	skeleton_name:   full path to skeleton
	"""

	# predict
	print(f'analyzing video: {video}')
	reader = VideoReader(video, batch_size=batch_size, gray=True, frame_size=model.input_shape)
	predictions = model.predict(reader, verbose=1, workers=1, use_multiprocessing=False)
	reader.close()

	# get column names
	features = list(pd.read_csv(skeleton_name).name)
	columns = []
	for f in features:
		columns += [f+'_x', f+'_y', f+'_confidence']

	# save to csv
	data = pd.DataFrame(columns=columns, index=np.arange(predictions.shape[0]))
	data[:] = np.reshape(predictions, (predictions.shape[0], -1))
	data.to_csv(os.path.splitext(video)[0] + '_tracking.csv')

	return predictions


def make_tracking_video(video, skeleton_name, predictions=None, fps=300, confidence_thresh=.1):
	"""
	make video showing tracking for already-tracked video
	assumes 'video_tracking.csv' exists if predictions not prvided
	video: 	  	     full path to video
	skeleton_name:   full path to skeleton
	predictions:	 (optional) array of predictions (n_frames X n_features X xy); if not provided loads from csv
	"""

	# todo: replace with matplotlib for subpixel resolution?

	# inits
	video_output = os.path.splitext(video)[0] + '_tracking.avi'
	print(f'making tracking video: {video_output}')
	if predictions is None:
		predictions = pd.read_csv(os.path.splitext(video)[0] + '_tracking.csv').to_numpy()[:,1:]
		predictions = predictions.reshape((-1, int(predictions.shape[1]/3), 3))  # (frane_num X feature_num X (x,y,confidence))
	skeleton = utils.initialize_skeleton(skeleton_name)
	graph = skeleton[["tree", "swap_index"]].values[:,0]
	cmap = plt.cm.hsv(np.linspace(0, 1, len(graph)))[:, :3][:, ::-1] * 255

	# make video
	reader = VideoReader(video, gray=False, batch_size=1)  # errs when great=True even for gray vids
	writer = VideoWriter(video_output, (reader[0].shape[2], reader[0].shape[1]), 'XVID', fps)  # 'XVID' works on windows // size is (width, height)

	for frame_num, frame, keypoints in tqdm.tqdm(zip(range(len(reader)), reader, predictions)):
		frame = frame[0].copy()

		# lines
		for idx, node in enumerate(graph):
			if node >= 0:
				pt1 = keypoints[idx]
				pt2 = keypoints[node]
				if pt1[-1]>confidence_thresh and pt2[-1]>confidence_thresh:
					cv2.line(frame, (int(pt1[0]), int(pt1[1])), (int(pt2[0]), int(pt2[1])), (0, 0, 255), 1, cv2.LINE_AA)
		# dots
		for idx, keypoint in enumerate(keypoints):
			if keypoint[-1]>confidence_thresh:
				keypoint = keypoint.astype(int)
				cv2.circle(frame, (keypoint[0], keypoint[1]), 2, tuple(cmap[idx]), -1, lineType=cv2.LINE_AA)
		# frame number
		frame = cv2.putText(frame, f'frame {frame_num}', (0,round(frame.shape[0]*.95)), cv2.FONT_HERSHEY_SIMPLEX, .5, (255, 255, 255))

		writer.write(frame)

	writer.close()
	reader.close()
