%% crop all the tank vids

% settings
rootDir = 'Z:\locker\ShareData\Chin_for_Dillon';


% get experiment folders
dirs = dir(rootDir); dirs = dirs([dirs.isdir]); dirs = {dirs(3:end).name};
for i = 1:length(dirs)
    % get subdirs
    subDirs = dir(fullfile(rootDir, dirs{i})); subDirs = subDirs([subDirs.isdir]); subDirs = {subDirs(3:end).name};
    for j = 1:length(subDirs)
        cropTankVid(fullfile(rootDir, dirs{i}, subDirs{j}, 'videoEOD.avi'));
    end
end