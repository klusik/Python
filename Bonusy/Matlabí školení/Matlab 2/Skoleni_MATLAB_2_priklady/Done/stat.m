function [ap, gp] = stat(x)

n = length(x);

ap = aprumer(x,n);
gp = gprumer(x,n);

end

function ya = aprumer(xa,na)

ya = sum(xa)/na;

end

function yg = gprumer(xg,ng)

yg = prod(xg)^(1/ng);

end
