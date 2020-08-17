"""
concatenates all videos to be included in training set
root_dir (command line argument) contains one dir per session, each containing >=1 video
in each session dir, all vids are concatenated into concatenated.avi
all these vids are then concatenated in root_dir\concatenated.avi
"""

import sys
import os
root_dir = sys.argv[1]
vid_folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]

# concat vids in individual folders
for vid_folder in vid_folders:
    # create .txt list of files to be concatenated
    vid_names = [f.name for f in os.scandir(vid_folder) if f.path.endswith('.avi') and f.is_file()]
    with open(os.path.join(vid_folder, 'list.txt'), 'w+') as file:
        file.writelines(['file '+v+'\n' for v in vid_names])

    # concat with ffmpeg
    command = '{} && cd {} && ffmpeg -y -f concat -safe 0 -i {} -c copy {}'.format(
        vid_folder[0]+':', vid_folder, 'list.txt', 'concatenated.avi')
    os.system(command)
    os.remove(os.path.join(vid_folder, 'list.txt'))

# concat across all vids
with open(os.path.join(root_dir, 'list.txt'), 'w+') as file:
    # create .txt list of files to be concatenated
    file.writelines([r'file '+vid_folder.replace('\\','\\\\')+'\\\\concatenated.avi'+'\n'  # windows is the worst...
                     for vid_folder in vid_folders])

# concat with ffmpeg
command = '{} && cd {} && ffmpeg -y -f concat -safe 0 -i {} -c copy {}'.format(
    root_dir[0] + ':', root_dir, 'list.txt', 'concatenated.avi')
os.system(command)
os.remove(os.path.join(root_dir, 'list.txt'))