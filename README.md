# fish_tracking
3d tracking of mormyrid fish in neuroscience experiments

# pipeline
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
  - watch videos generated with `predict\make_tracking_video.py` to identify frames to be added to the training set
  - use notebook `label\add_frames_to_dataset` to create a new dataset by combining them with an existing dataset


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
  - [ ] add bad frames and retrain
    - [X] write vids with frame nums
    - [X] find bad frames
    - [X] add bad frames to training set
    - [X] fix bad frame labels
    - [X] retrain
  - [ ] *make batch scripts*
  
- tank tracking
  - [ ] install anipose, make board
  - [ ] train networks
  - [ ] figure out calibration
  - [ ] figure out 3d reconstruction