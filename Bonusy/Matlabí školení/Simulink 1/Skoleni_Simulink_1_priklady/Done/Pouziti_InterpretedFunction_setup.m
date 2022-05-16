% Parametry - pocatecni vyska
x0 = 10;

% Grafika
% zavreni predchoziho okna
close(findobj('Tag','scena'))

% nove okno
figure('Position',[10 50 500 500],'Tag','scena');
axes
axis([0 3 -1 12])

% podlaha
rectangle('Position',[0 -1 3 1],'FaceColor',[0 0 0.8])

% teleso
teleso = rectangle('position',[1 x0 1 1],'FaceColor',[1 0.4 0]);
