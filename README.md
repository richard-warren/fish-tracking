# fish_tracking
3d tracking of mormyrid fish in neuroscience experiments

# pipeline
- create training set
  - run `label\concat_vids.py root_dir` to concatenate all vids to be included in training set
  - use jupyter notebook `initialize_training_set.ipynb` to initialize a to-be-labeled training set from the concatenated video
  - label by running `python label_data.py path_to_training_set path_to_skeleton`


# todo
- stim tracking
  - [X] concat all vids for training set
  - [X] make skeleton
  - [X] label training set
  - [X] train initial network
  - [ ] evaluation
    - [ ] make evaluation script
    - [ ] make evaluation vids
  - [ ] add bad frames and retrain
  - [ ] fix skeleton bug

- tank tracking
  - [ ] install anipose, make board
  - [ ] train networks
  - [ ] figure out calibration
  - [ ] figure out 3d reconstruction