"""
makes video showing DeepPoseKit tracking
give command line arguments: video, skelton (all with full paths)
"""


from predict.utils import make_tracking_video
import sys

video, skeleton_name = sys.argv[1:]
make_tracking_video(video, skeleton_name)