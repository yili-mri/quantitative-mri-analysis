%% single_pool_preparation_robustness.m
% Exploratory single-pool Bloch simulation comparing conventional and
% single-refocused CW-T1rho preparation over B0/B1 variation.
clear; clc; close all;

T1=1.0; T2=0.050; fSL=400; TSL=32e-3;
dfList=-300:5:300; b1List=0.75:0.01:1.25;
tp90=0.5e-3; tp180=1e-3;
rf90=1/(4*tp90); rf180=1/(2*tp180);
M0=[0;0;1];
Sc=zeros(numel(dfList),numel(b1List)); Sr=Sc;

for i=1:numel(dfList)
    for j=1:numel(b1List)
        df=dfList(i); b1=b1List(j);
        % Conventional: 90x - SL(+y) - 90(-x)
        M=prop(M0,b1*rf90,0,df,tp90,T1,T2);
        M=prop(M,b1*fSL,pi/2,df,TSL,T1,T2);
        M=prop(M,b1*rf90,pi,df,tp90,T1,T2);
        Sc(i,j)=abs(M(3));

        % Single refocus: 90x - SL(+y)/2 - 180y - SL(-y)/2 - 90x
        M=prop(M0,b1*rf90,0,df,tp90,T1,T2);
        M=prop(M,b1*fSL,pi/2,df,TSL/2,T1,T2);
        M=prop(M,b1*rf180,pi/2,df,tp180,T1,T2);
        M=prop(M,b1*fSL,-pi/2,df,TSL/2,T1,T2);
        M=prop(M,b1*rf90,0,df,tp90,T1,T2);
        Sr(i,j)=abs(M(3));
    end
end

figure; imagesc(b1List,dfList,Sc); axis xy; colorbar;
xlabel('B1 scale'); ylabel('B0 offset (Hz)');
title('Conventional preparation |M_z|');

figure; imagesc(b1List,dfList,Sr); axis xy; colorbar;
xlabel('B1 scale'); ylabel('B0 offset (Hz)');
title('Single-refocused preparation |M_z|');

fprintf('Fraction |Mz| >= 0.95: conventional %.2f%%, refocused %.2f%%\n', ...
    100*mean(Sc(:)>=0.95),100*mean(Sr(:)>=0.95));

function Mout = prop(Min,f1,phase,df,t,T1,T2)
R1=1/T1; R2=1/T2;
wx=2*pi*f1*cos(phase); wy=2*pi*f1*sin(phase); wz=2*pi*df;
A=[-R2 wz -wy; -wz -R2 wx; wy -wx -R1];
C=[0;0;R1];
P=expm([A C; zeros(1,4)]*t);
tmp=P*[Min;1]; Mout=tmp(1:3);
end
