%% Funkce
clc

% disp(the_best_function(1, 2, 3));

the_best_function(1, 2, 3);

% Zobrazit (vrátit) počet vstupů
% Možné použít na test, jestli je funkce správně
% parametrizovaná.

% Pro výstup je nargout
nargin('the_best_function');

varangin([1,2], [2,3], [3,4])


function varangin(varargin)
    for k = 1:length(varargin)
        x(k) = varargin{k}(1);
        y(k) = varargin{k}(2);
    end

    plot(x,y,'r')
end