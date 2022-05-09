%% PROMENNE %%

% bez diakritiky (ofc), nesmí začínat číslicí, je case sensitive 

%% HISTORIE %%

% Je možno použít CTRL pro výběr více příkazů z historie a vyvolat je
% najednou (najs!)

%% VEKTORY %%

% Matlab doplní do vektoru nuly, pokud daná pozice neexistuje (automaticky
% prostě roztáhne pole)

% Transpozice vektoru přes apostrof



step = 0.01;
x = 1:step:2;
y = sin(2*pi*x);

%plot(x,y);



% Násobení po prvcích -- tečka, např. x.*y 


x = 1:100;
y = log(x);

x.*y;


% Výběr z řádku a sloupce:

Matice = [1 2 3; 4 5 6; 7 8 9];

Matice([1 2], [2 3])

size(Matice)

% Násobení matic atd.
mg = magic(10);
mg10 = mg*10;

% Řešení soustavy lin. rovnic
% y = x + 1
% y = -2x + 4


Matice_soustava = [-1 1; 2 1];
vektor = [1 4]';

inv(Matice_soustava) * vektor

% MInimum v matici
minimum = min(Matice(:)) % Převést na vektor po prvcích a z toho


%% Grafika

% hold on / hold off -- nepřekreslení grafu

%% Zadání
% Vytvořte rand vektor s 10 prvky hodnoty mezi 0 a 1
% najděte všechny mezi 0.4 a 0.8

rand_vector = rand(100, 1)

logical_vector = rand_vector > 0.5 & rand_vector < 0.55

rand_vector(logical_vector)





