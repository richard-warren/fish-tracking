import argparse
import yaml
import sys
import os


# get args
parser = argparse.ArgumentParser()
parser.add_argument('-vid_type', type=str, default="free", help="free or fixed, depending on dataset type")
parser.add_argument('-root_dir', type=str, default=r"D:\\github\\fish-tracking\\", help="fish-tracking github repo location")
parser.add_argument('-brightness', type=float, default=1.0, help='adjust brightness by positive scalar multiple')
args = parser.parse_args()


# load config
with open(os.path.join(args.root_dir, 'config.yaml')) as f:
	cfg = yaml.safe_load(f)[args.vid_type]


print('dataset: ', cfg['dataset'])
print('skeleton:', cfg['skeleton'])

from deepposekit import Annotator
app = Annotator(datapath=cfg['dataset'],
                dataset='images',
                skeleton=cfg['skeleton'],
                shuffle_colors=True,
                text_scale=0.2,
                scale=1.0,
                brightness=args.brightness)

app.run()