%% Školení MATLAB 2

clear
clc


%% Další datové typy

% cell {}

cell_array = {[1, 2, 3], 'ahoj', "ahoj"};


cell_array(1);
cell_array{1};

array_of_arrays = {["něco"], cell_array};

array_of_arrays;

% struktury
clear

kruh.stred = [2 3];
kruh.polomer = 6;

S = pi*kruh(1).polomer^2;

kruh(2).stred = [5 4];
kruh(2).polomer = 10;

S = pi*kruh(2).polomer^2;




