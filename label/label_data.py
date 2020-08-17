from deepposekit import Annotator
import sys

# get arguments
dataset, skeleton = sys.argv[1:3] 
print(f'dataset: {dataset}')
print(f'skeleton: {skeleton}')

app = Annotator(datapath=dataset,
                dataset='images',
                skeleton=skeleton,
                shuffle_colors=False,
                text_scale=0.2)

app.run()