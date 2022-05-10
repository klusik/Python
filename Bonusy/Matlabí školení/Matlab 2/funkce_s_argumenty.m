function funkce_s_argumenty(a,b)
% Tuta funkce má argumenty

arguments
    a {mustBeNumeric} = 1
    b {mustBeNumeric} = 1
end

disp("Zadane hodnoty: " + a + " a " + b)