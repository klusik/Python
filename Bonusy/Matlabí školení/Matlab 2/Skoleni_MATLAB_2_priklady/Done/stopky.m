function stopky

persistent CAS

if isempty(CAS)
    CAS = datetime;
    disp(['start v ', datestr(CAS)])
else
    t = datetime - CAS;
    disp(t)
end
end