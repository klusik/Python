%% POKROCILE NASTAVENI GRAFU

% nacteni dat
load bode_data

%% Handle
% Pri vytvareni si uchovavam handle pro nasledne ovladani a nastavovani

% figure
hf = figure;

% axes
ha = axes;

% 3-D graf
hs = surf(w,ksi,magdb);

% do hf, ha a hs se ulozi odkazy na graficke objekty (tzv. handle), pomoci
% kterych lze graf nastavovat

%% Popisky

% zakladni popis os
xlabel('frekvence \omega [rad/s]')
ylabel('pomìrné tlumení \xi [-]')
zlabel('amplituda [dB]')
title('Frekvenèní charakteristika')

% pridava do figure textove objekty

%% Osy

% zmena osy X na logaritmickou
set(ha,'XScale','log')

% zmena smeru osy Y
set(ha,'YDir','reverse')

% pozice znacek - aby se nemenilo a bylo pevne fixovano
set(ha,'YTick',[0 1])
% zadanim se zmeni YTickMode z 'auto' na 'manual' => nebude se jiz
% automaticky menit (prizpusobovat velikosti okna, ...)

% popis
set(ha,'YTickLabel',{'0','1 = mez kmitavosti'})
% zadanim se zmeni YTickLabelMode z 'auto' na 'manual' => nebude se jiz
% automaticky menit (prizpusobovat velikosti okna, ...)

% alternativne lze zmenit pouze vybrane 
%  ha.YTickLabel(1) = {'text'}; 
%  nebo texty = get(...) > upravit texty > set(...)

% detailni ciselne nastaveni
set(ha,'YLim',[0 max(ksi)]) % == ylim([ymin ymax])
% zadanim se zmeni YLimMode z 'auto' na 'manual' => nebude se jiz
% automaticky menit (prizpusobovat velikosti okna, ...)

% pøíkaz axis: meni nastaveni rozsahu os pohromade - viz. doc axis

%% Mrizka

% grid on, grid off - zapnuti/vypnuti mrizky pro vsechny osy
% nastaveni XGrid, YGrid, .. pro jednotlive osy zvlast
set(ha,'GridLineStyle','-')

% Osa X ma zapnuty minor grid (XMinorGrid = 'on'), ktery se zapnul
% automaticky pri prepnuti do logaritmickeho meritka. Lze zapinat pro
% jednotlive osy a menit i MinorGridLineStyle = :

%% Pohled

[az,el] = view; % do az a el ulozi souradnice aktualniho pohledu

% view([0 0])
% view([45 0])
view([45 20])

%% Barvy

% barevna osa
colorbar

% barevna mapa: colormap hsv, colormap hot

% rozsah barev
set(ha,'CLim',[-20 10]) % == caxis([cmin cmax])

% interpolovane barvy
set(hs,'FaceColor','interp') % == shading interp

% barva car
% set(hs,'LineStyle','none')
set(hs,'EdgeColor',[0.5 0.5 0.5])
set(hs,'MeshStyle','row') % nebo 'column', 'both'

% pruhlednost
set(hs,'FaceAlpha',0.5)

% nasviceni a odlesky: light, camlight, lighting

%% Pridani dalsich grafu
hold on

% 3-D kontury
[~,hc] = contour3(w,ksi,magdb,30,'LineWidth',1);

% zvyrazneni car pro ksi == 0 (pozice 7) a w == wn (pozice 50)
hp1 = plot3(w,ones(size(w)),magdb(7,:),'r','LineWidth',2);

hp2 = plot3(wn*ones(size(ksi)),ksi,magdb(:,50),...
    'Color',[0 0 0.5],...
    'LineStyle','-',...
    'LineWidth',1,...
    'Marker','^',...
    'MarkerEdgeColor',[0 0 1],...
    'MarkerFaceColor',[0 1 1],...
    'MarkerSize',10);

% pozn. hledani pozice prikazem idx = find(w==wn) neni pro datovy typ
% double vhodne, lepsi je pouzit [~,idx] = min(abs(w-wn)) nebo
% idx = find(abs(w-wn)<tol)

%% Uprava polohy axesu
set(ha,'Position',[0.1 0.4 0.75 0.5])

%% Druhy axes
ha2 = axes('Position',[0.1 0.1 0.35 0.15]);
semilogx(w,magdb)
grid
axis tight
xlabel('frekvence \omega [rad/s]')
ylabel('amplituda [dB]')

ha3 = axes('Position',[0.6 0.1 0.35 0.15]);
semilogx(w,phase)
grid
axis tight
xlabel('frekvence \omega [rad/s]')
ylabel('fáze [deg]')

linkaxes([ha2 ha3],'x')

%%
set(hf,'Position', [50 100 700 700]);