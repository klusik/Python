function pN = posunTelesa(pN,teleso)

% aktualni pozice obdelniku
p = get(teleso,'Position');

% posun obdelniku do nove Y-pozice pN
p(2) = pN;
set(teleso,'Position',p)

drawnow;