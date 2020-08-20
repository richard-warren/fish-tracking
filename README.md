# fish_tracking
3d tracking of mormyrid fish in neuroscience experiments

# pipeline
- create training set
  - run `python label\concat_vids.py root_dir` to concatenate all vids to be included in training set
  - use jupyter notebook `label\initialize_training_set.ipynb` to initialize a to-be-labeled training set from the concatenated video
  - label by running `python label\label_data.py path_to_training_set path_to_skeleton`
- train model
  - use jupyter notebook `train\train.ipynb`
- evaluate
  - evaluate a single video with `python predict\analyze_video.py video_name model_name skeleton_name`
    - `video_name_tracking.csv` is generated in the video's directory
  - create a video showing tracking `python predict\make_tracking_video.py video_name skeleton_name`
     - `video_name_tracking.avi` is generated in the video's directory (assumes `video_name_tracking.csv` exists)


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
  - [ ] *add bad frames and retrain (do i need to make new gui???)*
  - [ ] make batch scripts
  
- tank tracking
  - [ ] install anipose, make board
  - [ ] train networks
  - [ ] figure out calibration
  - [ ] figure out 3d reconstruction