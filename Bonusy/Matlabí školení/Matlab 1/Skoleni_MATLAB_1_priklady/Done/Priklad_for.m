x(1) = 1;

for k = 2:100
    x(k) = 0.9*x(k-1);
end

plot(x)