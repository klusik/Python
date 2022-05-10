x = -2*pi:pi/10:2*pi;
y = -2*pi:pi/5:2*pi;
 
[X,Y] = meshgrid(x,y);
 
R = sqrt(X.^2+Y.^2); % zabrani deleni nulou a vzniku NaN
Z = sin(R)./R;
 
% Plot
 
subplot(2,2,1)
mesh(X,Y,Z);
 
subplot(2,2,2)
surf(X,Y,Z);
 
subplot(2,2,3)
contour(X,Y,Z);

subplot(2,2,4)
contour3(X,Y,Z);
