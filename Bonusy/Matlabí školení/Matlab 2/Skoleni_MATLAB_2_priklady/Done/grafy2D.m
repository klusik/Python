%% Graf se zvyraznenymi body, carou a textem

x = linspace(0,pi,100);
y = sin(x);

xm = 0:pi/4:pi; % znacky v bodech x
ym = sin(xm);

figure
plot(x,y)
hold on
plot(xm,ym,'*')
axis tight

% Cara v hodnote prumeru

m = mean(y);

hA = gca;
xlimits = hA.XLim;

hL = line([xlimits(1),xlimits(2)],[m,m]);

hL.Color = [1 0.5 0.5];
hL.LineWidth = 2;
hL.LineStyle = '--';

% Legenda pouze pro dany objekt

legend(hL,'mean of data')

% Pridani textu

text(xm(2),ym(2),'  \leftarrow sin(\pi/4) = 0.71')

text(1.2,0.58,['mean value is ',num2str(m)])

%% Zobrazeni rovnice v grafu

x = linspace(0,3);
y = x.^2.*sin(x);

figure
plot(x,y)
line([2,2],[0,2^2*sin(2)])

str = '$$ \int_{0}^{2} x^2\sin(x) dx $$';
text(1.2,0.5,str,'Interpreter','latex')

%% Graf se dvema osami Y

A = 1200;
a = 0.005;
b = 0.005;

x = 0:900;
y1 = A*exp(-a*x);
y2 = sin(b*x);

figure
[hA,hP1,hP2] = plotyy(x,y1,x,y2);

% Popisky
ylabel(hA(1),'exp') % popis leve osy Y
ylabel(hA(2),'sine') % popis prave osy Y

xlabel('Time') % popis osy X

% Axis
axis(hA(1),[0 900 0 1200])

% Grid
grid(hA(1),'on')

% Zmena vzhledu car
hP1.LineStyle = '--';
hP1.LineWidth = 2;
hP2.LineWidth = 2;

%% Graf se dvema osami Y - odlisny typ grafu

figure
[hA,hP1,hP2] = plotyy(x,y1,x,y2,'semilogy','plot');

grid(hA(1),'on')

grid(hA(1),'off')
grid(hA(2),'on')

% viz. doc plotyy

%% Graf s vice osami X a Y

load multiaxData

% jak data vypadaji?
% figure
% plot(x1,y1)
% figure
% plot(x2,y2)

% Tvorba pozadovaneho grafu
figure
line(x1,y1,'Color','r') % funkce plot zde neni vhodna - prizpusobuje axes

hA1 = gca; % aktualni axes
hA1.XColor = 'r'; % zmena barvy osy
hA1.YColor = 'r'; % zmena barvy osy

pos = hA1.Position; % poloha prvniho axesu
hA2 = axes('Position',pos,...
    'XAxisLocation','top',...
    'YAxisLocation','right',...
    'Color','none');

line(x2,y2,'Color','k')

%% Maly graf ve velkem

% Prostym vytvorenim dvou nezavislych axesu
figure
hA1 = axes;
plot(x1,y1);

hA2 = axes('Position',[0.55 0.55 0.3 0.3]);
plot(x2,y2,'r');
grid on

%% Kombinace sloupcoveho a caroveho grafu - odlisne osy Y

% data concentrace a teploty mereny kazdych 5 dnu po dobu 35 dnu

load barlineData

figure
[hA,hB,hL] = plotyy(days,temp,days,conc,'bar','plot');

title('Trend Chart for Concentration')
xlabel('Day')
ylabel(hA(1),'Temperature (^{o}C)')
ylabel(hA(2),'Concentration')

hL.LineWidth = 3;
hL.Color = [0,0.7,0.7];

%% Barevne zvyrazneni intervalu

% Uzitecne pro vizualizaci intervalu spolehlivosti, ...

load errorData

% stredni hodnota a smerodatna odchylka
m = mean(y);
e = std(y);

figure
axes
hold on

x = 1:length(m);
xp = [x flip(x)];
yp = [m+e, flip(m-e)];

hPA = patch(xp,yp,[0.9 0.9 0.9]);
hPA.EdgeColor = 'none';

hP(1) = plot(m,'LineWidth',2);
hP(2) = plot(m+e,'r--');
hP(3) = plot(m-e,'r--');

hold off

legend(hP,'mean','mean + 1*STD','mean  - 1*STD','Location','southeast')

%% Casova osa

% Manualni prace s retezci v cell array ... nepohodlne

% Nove datove typy od R2014b
%  * datetime
%  * duration, calendarDuration
%  * years, days, hours, minutes, seconds
%  * calyears, calquarters, calmonths, calweeks, caldays

load finData

figure
plot(dates,data)

xlabel('Date')
ylabel('Index Value')
title ('Normalized Daily Index Closings')
legend(series, 'Location', 'NorthWest')

%  zmena meritka grafu meni casove znacky: roky-mesice-dny-hodiny-...
