from deepposekit import Annotator
import sys

# get arguments
dataset, skeleton = sys.argv[1:3]
if len(sys.argv)==4:  # optional third arg for image brightness
	brightness = float(sys.argv[3])
else:
	brightness = 1.0

print(f'dataset: {dataset}')
print(f'skeleton: {skeleton}')

app = Annotator(datapath=dataset,
                dataset='images',
                skeleton=skeleton,
                shuffle_colors=True,
                text_scale=0.2,
                scale=1.0,
                brightness=brightness)

app.run()