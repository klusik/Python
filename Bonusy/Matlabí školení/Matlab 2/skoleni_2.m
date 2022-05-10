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

kruh(2);

% Struktury mohu spojovat jen tehdy, 
% když mají stejná jména položek
% (je to klasické pole)

% Získání všech položek

kruh.polomer;

% Vrací 'comma separated list'
% 3, 8 vrátí do ans 3 a pak 8

cat(kruh.polomer);

% Table
table_of_cicies = readtable('NejvetsiMestaCR.xlsx');

% Summary vrátí "various info" o tabulce (cool)
% summary(table_of_cicies);

%% Hodiny a stuff
clock;

now;

date;

datestr(now);

% Daytime a duration

time_1 = datetime;
time_2 = datetime(1984, 1, 1);

% Daytime můžu přes tečky jako time_2.hour 
% a podobně (yes)

% Jak dlouho od mýho narození?
years_from_my_birthday = years(time_1 - time_2);

%% Categorical

some_array = {'1', '2', 'a'};

cat_some_array = categorical(some_array);

categories(cat_some_array);
nnz(cat_some_array == '2');

%% Sparse matrices









