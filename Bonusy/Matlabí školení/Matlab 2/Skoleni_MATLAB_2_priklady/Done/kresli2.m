function [x0,y0] = kresli2(x,a,b)

arguments
    x (1,:) double              % přijímá řádkové i sloupcové vektory
    a (1,1) {mustBeNumeric} = 1
    b (1,1) {mustBeNumeric} = 0
end

y = a*x+b;
 
if nargout == 0
    plot(x,y,'-o');
else
    x0 = x;
    y0 = y;
end

end
