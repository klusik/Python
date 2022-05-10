x = [];
a = input('Zadej a: ');

while a ~= 0
    x = [x,a];
    a = input('Zadej a: ');
end

disp(x)