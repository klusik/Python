function y = funkce_s_chybou_upraveno(a,b,c,x)
%FUNKCE_S_CHYBOU je kvadratická funkce zadaná parametry a bodem
%   Y = FUNKCE_S_CHYBOU(A,B,C,X) vypočte hodnoty rovnice Y = AX^2+BX+C pro
% hodnoty X. Vykreslí křivku, která spojuje body s x-ovými souřadnicemi
% danými vektorem X a y-ovými souřadnicemi danými vektorem Y a přidá název
% grafu ve tvaru 'y = ax^2 + bx + c', kde 'a', 'b' a 'c' jsou dány
% vstupními parametry.
% Příklad: Nalezněte tři chyby, které FUNKCE_S_CHYBOU obsahuje.
% Po zavolání Y = FUNKCE_S_CHYBOU(5,2,1,1:10) by funkce měla vykreslit
% graf křivky spojující body o souřadnicích [x,y], pro x = 1:10 a k nim
% odpovídající y=5x^2+2x+1, a přidat ke grafu název 'y=5x^2+2x+1'.

%% Výpočet
try
    y=a*x.^2+b*x+c;
catch
    error('Něco se pokazilo. Zadal jsi vstupy?')
end


%% Vykreslení grafu
plot(x,y)

%% Přidání názvu grafu
s1 = 'y = ';
s2 = 'x^2 + ';
s3 = 'x + ';
sa = num2str(a);
sb = num2str(b);
sc = num2str(c);
str = [s1, sa, s2, sb, s3, sc];
title(str)


end