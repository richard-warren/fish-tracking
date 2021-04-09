# fish-tracking
This repo contains scripts for training and deploying `DeepPoseKit` models to analyze freely moving (head-free) and head-fixed fish.


## general
This repo uses [rick's fork](https://github.com/richard-warren/deepposekit) of the `DeepPoseKit` repo. All of the dependencies are set up in the `dpk` environment in `Anaconda`. Most scripts are run interactively in `jupyter` notebooks.

To prevent you from having to change a bunch of variables across different `jupyter` notebooks, many notebooks read from `config.yaml`. Here you can specify (for both head-free and head-fixed experiments) the trained `model` to use for analysis, the `data_dir` where the videos are located, the file defining the `skeleton` of the fish, and the training `dataset`.  

To get started, open an `Anaconda` prompt and activate the `dpk` environment:
```
activate dpk
```
Then navigate to the local `github` repo ad launch `jupyter`:
```
D:
cd github\fish-tracking
jupyter notebook
```
Details on labeling data, training models, and using models for prediction are found below.

**Note:** One important change in rick's modification of the `DeepPoseKit` repo is the addition of more metadata to the frames included in datasets. Specifically, I added `video_name` and `frame_number` fields. Not all of the code in the repo has been updated to expect these fields, although all the scripts currently in use do. If you run into errors this is an avenue to explore.


## label
The `label` folder contains scripts for creating and labeling datasets.

#### label an existing dataset
`label\label_data.py` is a wrapper for the `DeepPoseKit` labeling GUI. It allows you to label the dataset specified in `config.yaml` and located in `label\datasets`. Using your command line super-powers launch the GUI as follows:
```
label\label_data.py
```
Add an `-h` flag to see some convenient command line options (e.g. brightness adjustment):
```
label\label_data.py -h
```

#### add new frames to a dataset
There are some scripts for automatically determining frames to be included in an expanded dataset based on confidence heuristics. However, we have settled on manually identifying frames. The following pipeline is only set up for the head-free videos.

Modify `label\c1_tracking_errors.csv` to include only new videos and frames to be included. You can delete old entries, as they are saved in a google doc. Then open the `label\add_frames_manually` notebook. Run the cells under the **add frames from spreadsheet** heading after modifying the `old_dataset` and `merged_dataset` fields. This will create a new `merged_dataset` that combines the frames you identified with those in the `old_dataset`.

If interested, the other notebooks in the `label` folder contain code for:
- `label\add_frames_automatically`
   - finding frames automatically from a specified video based on confidence heuristics
- `label\make_training_set`
  - initializing a new dataset via k-means clustering on a single video
  - modifying the skeleton for an existing dataset
  - renaming body parts in a skeleton file and/or the skeleton data embedded in a dataset
- `label\add_frames_manually`
  - the first chunk of code in this notebook allows you to specify frames from a single video to be added to the training set (as opposed to adding frames from across videos that are specified in a spreadsheet).


## train
- Work through the cells in the `train\train` notebook to train a new network, following the documentation as you go. The model will be saved in `train\models` (this overwrites the previous model by default!).


## predict
You can analyze videos using the `predict\analyze_videos` notebook. Most scripts automatically generate a video showing the tracking, which has the same name but appended with `_tracking.avi`. You can either:
- **analyze a single video** by specifying it's name, the model, and the skeleton you would like to use.
- **analyze all folders for a project**. This will comb through all the videos in the head-fixed or head-free experiments and analyze everything.
- **analyze user-specified head-free folders**. This will analyze a list of videos you specify.

If interested:
- `predict\analyze_video.py` and `predict\make_tracking_video.py` and wrappers that analyze and make tracking videos for specific videos. These can be run from the command line.
