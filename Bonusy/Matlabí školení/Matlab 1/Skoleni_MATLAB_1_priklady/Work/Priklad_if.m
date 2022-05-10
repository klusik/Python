% ax^2 + bx + c = 0

a = input('Zadej a: ');
b = input('Zadej b: ');
c = input('Zadej c: ');

D = b^2-4*a*c;

if D == 0
    disp('Koren je dvojnasobny.')
elseif D > 0
    disp('Koreny jsou realne ruzne.')
else
    disp('Koreny jsou komplexni.')
end