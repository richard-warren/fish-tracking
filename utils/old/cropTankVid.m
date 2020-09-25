function cropTankVid(vidName, varargin)

% crops a video by removing sections without a fish from the beginning and
% the end of the video

% todo:
% add overwrite check option (to avoid recreating vids)
% separate vids for dft epochs?
% corresponding crops to the metadata? is this necessary?

% settings
s.thresh = 3.0;         % (z scored pixels) difference between frame and background frame for fish detection
s.avgSamples = 100;     % how many frames to sample when computing background image
s.buffer = 1;           % (s) time before and after fish appearance to keep
s.plotResults = true;   % whether to plot the results
s.medFiltering = .5;    % (s) median filter the thresholded signal to remove short periods
s.resolution = .1;      % (s) only sample frames ~ every s.resolution seconds
s.bitRate = 12;         % (megabits per second)



% initializations
if exist('varargin', 'var'); for i = 1:2:length(varargin); s.(varargin{i}) = varargin{i+1}; end; end
fprintf('cropping %s... ', vidName);
vid = VideoReader(vidName);
[path, name, ext] = fileparts(vidName);
croppedVidName = fullfile(path, [name '_cropped' ext]);
skipFrames = round(s.resolution * vid.FrameRate);
bufferSmps = round(s.buffer * vid.FrameRate / skipFrames);


% get median frame
fprintf('computing background... ')
numFrames = vid.NumFrames;
frames = zeros(s.avgSamples, vid.Height, vid.Width);
frameNums = floor(linspace(1, min(numFrames, round(5*60*vid.FrameRate)), s.avgSamples));  % don't take frames after the first 5 minutes
for i = 1:length(frameNums); frames(i,:,:) = rgb2gray(read(vid, frameNums(i))); end
background = double(squeeze(median(frames,1)));
bgStd = std(background(:));


% get diffs between each frame and background
fprintf('computing frame diffs... ')
frameNums = 1:skipFrames:numFrames;
diffs = nan(1, length(frameNums));
for i = 1:length(frameNums)
    try
        bgSub = double(rgb2gray(read(vid, frameNums(i)))) - background;
        diffs(i) = mean(abs(bgSub(:)));
    catch; end
end
diffs = diffs-mean(bgStd) / bgStd;  % !!! this should have parens around subtraction :/


% find start and end
thresholded = diffs>s.thresh;
thresholded = medfilt1(double(thresholded), round(s.medFiltering*vid.FrameRate/skipFrames)) == 1;

if ~any(thresholded)
    fprintf('WARNING! Fish not detected! No video created.\n')
    return
end

startInd = max(1, find(thresholded, 1, 'first') - bufferSmps);
endInd   = min(length(frameNums), find(thresholded, 1, 'last') + bufferSmps);
startTime = (frameNums(startInd)-1) * (1/vid.FrameRate);
endTime = (frameNums(endInd)-1) * (1/vid.FrameRate);


% plot results
if s.plotResults
    figure('name', vidName, 'color', 'white', 'menubar', 'none', ...
        'position', [215.00 551.00 1123.00 324.00]); hold on
    x = linspace(0, vid.Duration, length(frameNums));
    plot(x, diffs)
    xLims = [x(1) x(end)]; yLims = ylim;
    
    plot(xLims, [s.thresh s.thresh], 'color', [1 .1 .1])     % threshold
    plot([startTime startTime], yLims, 'color', [.6 .6 .6])  % start time
    plot([endTime endTime], yLims, 'color', [.6 .6 .6])      % end time
    
    xlabel('time (s)')
    ylabel('abs(frame - background) (z scored)')
    set(gca, 'box', 'off', 'xlim', xLims, 'ylim', yLims)
end


% crop video with ffmpeg\
fprintf('cropping between %.2f and %.2f... ', startTime, endTime);
command = sprintf('ffmpeg -i %s -ss %.2f -t %.2f -vb %iM -y -loglevel panic -stats %s', ...
                  vidName, startTime, endTime-startTime, s.bitRate, croppedVidName);
[~,~] = system(command);
fprintf('all done!\n')

              
              