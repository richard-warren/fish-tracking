"""
analyzes a video using DeepPoseKit
give command line arguments: video, model_name, skelton (all with full paths)
"""

from deepposekit.models import load_model
from predict.utils import analyze_video 
import sys

video, model_name, skeleton = sys.argv[1:]
model = load_model(model_name)
analyze_video(video, model, skeleton)