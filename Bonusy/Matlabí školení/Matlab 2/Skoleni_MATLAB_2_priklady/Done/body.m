function body(varargin)
 
for k = 1:length(varargin)
    x(k) = varargin{k}(1);
    y(k) = varargin{k}(2);
end
 
plot(x,y,'r*')
