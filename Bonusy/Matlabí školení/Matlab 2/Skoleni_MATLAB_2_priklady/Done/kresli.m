function [x,y] = kresli(x,a,b)
 
if nargin < 3
    b = 0;
    warning('Neni zadano b: b=0')
end
 
if nargin < 2
    a = 1;
    warning('Neni zadano a: a=1')
end
 
if nargin < 1
    error('Neni zadan zadny vstup')
end
 
y = a*x+b;
 
if nargout == 0
    plot(x,y);
else
    x0 = x;
    y0 = y;
end
