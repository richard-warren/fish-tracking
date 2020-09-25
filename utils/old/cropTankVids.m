%% crop all the tank vids

% settings
rootDir = 'Z:\locker\ShareData\Chin_for_Dillon';


% get experiment folders
dirs = dir(rootDir); dirs = dirs([dirs.isdir]); dirs = {dirs(3:end).name};
for i = 5:length(dirs)
    % get subdirs
    subDirs = dir(fullfile(rootDir, dirs{i})); subDirs = subDirs([subDirs.isdir]); subDirs = {subDirs(3:end).name};
    for j = 1:length(subDirs)
        cropTankVid(fullfile(rootDir, dirs{i}, subDirs{j}, 'videoEOD.avi'));
    end
end

%% count video read time

vid = VideoReader('Z:\locker\ShareData\Chin_for_Dillon\20200903\time_h16m53s53\videoEOD.avi');
numFrames = vid.numFrames;

tic
for i = 1:numFrames
    frame = read(vid, i);
end
fprintf('%.2f frames per second', numFrames / toc)
