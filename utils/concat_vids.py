"""
given root_dir (cli), which contains sub_dirs each containing videos,
concatenates all videos into 'concatenated.avi', placed in root_dir
if second cli is given, only videos are included which contain this string 
"""

import sys
import os
root_dir = sys.argv[1]
contains = '' if len(sys.argv)!=3 else sys.argv[2]  # only include vids containing this string
vid_folders = [f.path for f in os.scandir(root_dir) if f.is_dir()]

# concat vids in individual folders
with open(os.path.join(root_dir, 'list.txt'), 'w+') as file:
    for vid_folder in vid_folders:
        vid_names = [f.name for f in os.scandir(vid_folder) 
                     if f.path.endswith('.avi') and f.is_file() and contains in f.name]
        file.writelines(['file {}\n'.format(os.path.join(root_dir, vid_folder, v).replace('\\','\\\\')) for v in vid_names])

# concat with ffmpeg
command = '{} && cd {} && ffmpeg -y -f concat -safe 0 -i {} -c copy {}'.format(
    root_dir[0] + ':', root_dir, 'list.txt', 'concatenated.avi')
print(command)
os.system(command)
os.remove(os.path.join(root_dir, 'list.txt'))