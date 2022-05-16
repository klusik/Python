%% Zadani parametru pro model brzdeni kola

m = 300;    %kg
r = 0.25;   %m
g = 9.81;   %m/s2
J = 0.47;   %kg*m2
v0 = 27;    %m/s
% M = 500;  %N*m

%% Tabulka hodnot funkce skluz - soucinitel treni mi

skluz = 0:0.05:1;
mi = [0 0.4 0.8 0.97 1.0 0.98 0.96 0.94 0.92 0.9 0.88 0.855 0.83 0.81 0.79 0.77 0.75 0.73 0.72 0.71 0.7];

%% Vykresleni grafu zavislosti soucinitele treni na skluzu
plot(skluz,mi)
xlabel('skluz')
ylabel('mi')
title('SUCHY ASFALT')

