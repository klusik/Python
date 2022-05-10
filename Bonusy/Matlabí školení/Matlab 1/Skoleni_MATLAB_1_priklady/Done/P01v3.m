%  Grafy funkci
%
%    - sinus a cosinus
 
% priprava dat
x = 0:pi/20:2*pi;
y = sin(x);
y1 = cos(x);
 
figure % nove graficke okno
 
% vykresleni grafu
plot(x,y)
hold on
plot(x,y1)
 
title('Graf')
xlabel('osa x')
ylabel('osa y')
 
axis tight
grid on
 
legend('sin(\alpha)','cos(\alpha)')
