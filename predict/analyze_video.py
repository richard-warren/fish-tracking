import argparse
import os


# parse args
parser = argparse.ArgumentParser()
parser.add_argument('video', help="video to analyze")
parser.add_argument('model', help="DeepPoseKit model")
parser.add_argument('skeleton', help="skeleton file")
parser.add_argument('-batch_size', type=int, default=16, help="analysis batch size")
parser.add_argument('-makevideo', help="make tracking video", action='store_true')
parser.add_argument('-overwrite', help="overwrite existing files", action='store_true')
args = parser.parse_args()


# analyze video
outfile = os.path.splitext(args.video)[0] + '_tracking.csv'  # name of to-be-created tracking file
if args.overwrite or not os.path.exists(outfile):
	from utils import analyze_video, make_tracking_video
	predictions = analyze_video(args.video, args.model, args.skeleton, batch_size=args.batch_size)
	if args.makevideo:
		make_tracking_video(args.video, args.skeleton, predictions=predictions)  # add back predictions
# else:
# 	print('Warning! File already exists. Aborting. Use -overwrite flag to overwrite the file.')
