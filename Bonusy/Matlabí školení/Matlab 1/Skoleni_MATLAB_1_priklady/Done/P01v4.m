%  Grafy funkci
%
%    - sinus a cosinus
 
% priprava dat
x = 0:pi/20:2*pi;
y = sin(x);
y1 = cos(x);
 
figure % nove graficke okno
 
% vykresleni grafu
subplot(2,1,1)
plot(x,y) % doplneni - specifikace cary: plot(x,y,'b*:')
subplot(2,1,2)
plot(x,y1) % doplneni - specifikace cary: plot(x,y1,'ro-')
