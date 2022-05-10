function [zn,an] = signum(n)

%SIGNUM   Znamenko a absolutni hodnota.
%
% [ZN,AN] = SIGNUM(N) vraci znamenko ZN a absolutni hodnotu AM cisla N.

zn = sign(n);
an = abs(n);

