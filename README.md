# fish_tracking
3d tracking of mormyrid fish in neuroscience experiments

# training networks
- set up configuration
  - to avoid having to pass around a bunch of command line arguments, several global variables are defined in `config.yaml` and are accessed by some of the batch scripts
- create training set
  - run `python label\concat_vids.py root_dir` to concatenate all vids to be included in training set
  - use notebook `label\initialize_training_set.ipynb` to initialize a to-be-labeled training set from the concatenated video
  - label by running `python label\label_data.py path_to_training_set path_to_skeleton`
- train model
  - use notebook `train\train.ipynb`
- evaluate
  - evaluate a single video with `python predict\analyze_video.py video_name model_name skeleton_name`
    - `video_name_tracking.csv` is generated in the video's directory
  - create a video showing tracking `python predict\make_tracking_video.py video_name skeleton_name`
     - `video_name_tracking.avi` is generated in the video's directory (assumes `video_name_tracking.csv` exists)
- expand training set
  - manually
    - watch videos generated with `predict\make_tracking_video.py` to identify frames to be added to the training set
    - use notebook `label\add_frames_manually` to create a new dataset by combining them with an existing dataset
  - automatically
    - use notebook `label\add_frames_automatically` to identify poorly tracked frames based on confidence levels. creates a new dataset by combining them with an existing dataset.

# evaluating
- use `predict\analyze_video.py video model_name skeleton_name` to analyze a video from the command line

# todo
- stim tracking
  - [X] concat all vids for training set
  - [X] make skeleton
  - [X] label training set
  - [X] train initial network
  - [X] fix skeleton bug
  - [X] evaluation
    - [X] evaluation script
    - [X] evaluation vids
  - [X] add corner mirror feature
  - [X] retrain with brightness augmentation // regenerate predictions
  - [X] add bad frames and retrain
    - [X] write vids with frame nums
    - [X] find bad frames
    - [X] add bad frames to training set
    - [X] fix bad frame labels
    - [X] retrain
  - [ ] modify batch scripts (one function call per vid to avoid crashing problem... try loading model de novo in analyze_video function to avoid kernel crashing in jupyter?)
  - [ ] retrain with refined tip points?

- tank tracking
- [ ] **finalize bit rate**
- [X] finalize skeleton
  - [X] train models
    - [X] crop vids
    - [X] test opencv crop speed
    - [X] more aggressive cropping (python)
    - [X] concat all fish vids within a day
    - [X] label and train initial network
  - [ ] **refactor evaluation scripts**
  - [ ] install anipose, make board
  - [ ] figure out calibration
  - [ ] figure out 3d reconstruction
