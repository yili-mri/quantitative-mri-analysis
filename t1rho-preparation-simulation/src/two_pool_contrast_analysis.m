%% two_pool_contrast_analysis.m
% Generic two-mobile-pool Bloch-McConnell simulation of preparation-
% dependent apparent T1rho and target-reference tissue contrast.
clear; clc; close all;

SL=500; TSL=[0 10 20 40]*1e-3;
tp90=200e-6; tp180=400e-6; RF90=1/(4*tp90); RF180=RF90;
T1A=1; T1B=1; T2A=.050; T2B=.050;
ppm=1:.5:5; dfList=ppm*(42.57747892*3);
fBList=.05:.01:.20; kList=500:100:3000;
refF=.05; refK=1000;
sz=[numel(kList),numel(fBList),numel(dfList)];
TC=nan(sz); TR=TC; R2C=TC; R2R=TC; DC=TC; DR=TC;
TrefC=nan(size(dfList)); TrefR=TrefC;

for id=1:numel(dfList)
    df=dfList(id); fA=1-refF; kAB=(refF/fA)*refK;
    [TrefC(id),~]=simulate('conv',fA,refF,kAB,refK,df,T1A,T2A,T1B,T2B,SL,TSL,RF90,RF180,tp90,tp180);
    [TrefR(id),~]=simulate('ref', fA,refF,kAB,refK,df,T1A,T2A,T1B,T2B,SL,TSL,RF90,RF180,tp90,tp180);
    for ik=1:numel(kList)
        for jf=1:numel(fBList)
            fB=fBList(jf); fA=1-fB; kBA=kList(ik); kAB=(fB/fA)*kBA;
            [TC(ik,jf,id),R2C(ik,jf,id)]=simulate('conv',fA,fB,kAB,kBA,df,T1A,T2A,T1B,T2B,SL,TSL,RF90,RF180,tp90,tp180);
            [TR(ik,jf,id),R2R(ik,jf,id)]=simulate('ref', fA,fB,kAB,kBA,df,T1A,T2A,T1B,T2B,SL,TSL,RF90,RF180,tp90,tp180);
            Cc=1000*(TC(ik,jf,id)-TrefC(id));
            Cr=1000*(TR(ik,jf,id)-TrefR(id));
            DC(ik,jf,id)=Cr-Cc;
            rc=2*(TC(ik,jf,id)-TrefC(id))/(TC(ik,jf,id)+TrefC(id));
            rr=2*(TR(ik,jf,id)-TrefR(id))/(TR(ik,jf,id)+TrefR(id));
            DR(ik,jf,id)=rr-rc;
        end
    end
end

fprintf('\nFit-quality-filtered absolute contrast\n');
for th=[.99 .995 .999]
    mask=isfinite(DC)&R2C>=th&R2R>=th; v=abs(DC(mask));
    fprintf('R2 >= %.3f: retained %.2f%%, mean |DeltaC| %.4f ms, median %.4f ms, max %.4f ms\n', ...
        th,100*mean(mask(:)),mean(v),median(v),max(v));
    fprintf('  >0.5 ms %.2f%%, >1 ms %.2f%%, >2 ms %.2f%%\n', ...
        100*mean(v>.5),100*mean(v>1),100*mean(v>2));
end

mask=R2C>=.999&R2R>=.999;
x=abs(DC(mask)); y=abs(DR(mask)); R=corrcoef(x,y);
fprintf('Correlation |DeltaC| vs |DeltaRRTD| for R2 >= .999: %.6f\n',R(1,2));

M=abs(DC); M(~mask)=NaN;
figure; imagesc(fBList,kList,max(M,[],3)); axis xy; colorbar;
xlabel('Target pool fraction f_B'); ylabel('Target k_{BA} (s^{-1})');
title('Maximum |DeltaC| with both R^2 >= 0.999 (ms)');

figure; scatter(x,y,18,'filled'); grid on;
xlabel('|DeltaC| (ms)'); ylabel('|DeltaRRTD|');
title('Absolute versus relative contrast effect, R^2 >= 0.999');

function [T,R2]=simulate(prep,fA,fB,kAB,kBA,dfB,T1A,T2A,T1B,T2B,SL,TSL,RF90,RF180,tp90,tp180)
M0=[0;0;fA;0;0;fB]; S=zeros(size(TSL));
for q=1:numel(TSL)
    t=TSL(q); M=BM(M0,RF90,0,0,dfB,tp90,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA);
    if strcmp(prep,'conv')
        if t>0, M=BM(M,SL,pi/2,0,dfB,t,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA); end
        M=BM(M,RF90,pi,0,dfB,tp90,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA);
        S(q)=M(3)+M(6);
    else
        if t>0, M=BM(M,SL,pi/2,0,dfB,t/2,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA); end
        M=BM(M,RF180,pi/2,0,dfB,tp180,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA);
        if t>0, M=BM(M,SL,-pi/2,0,dfB,t/2,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA); end
        M=BM(M,RF90,0,0,dfB,tp90,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA);
        S(q)=-(M(3)+M(6));
    end
end
[T,R2]=fitrho(TSL,S);
end

function Mout=BM(M,f1,ph,dfA,dfB,t,T1A,T2A,T1B,T2B,fA,fB,kAB,kBA)
wx=2*pi*f1*cos(ph); wy=2*pi*f1*sin(ph); wA=2*pi*dfA; wB=2*pi*dfB;
AA=[-1/T2A-kAB wA -wy; -wA -1/T2A-kAB wx; wy -wx -1/T1A-kAB];
BB=[-1/T2B-kBA wB -wy; -wB -1/T2B-kBA wx; wy -wx -1/T1B-kBA];
A=[AA kBA*eye(3); kAB*eye(3) BB];
C=[0;0;fA/T1A;0;0;fB/T1B];
P=expm([A C;zeros(1,7)]*t); z=P*[M;1]; Mout=z(1:6);
end

function [T,R2]=fitrho(TSL,S)
T=NaN; R2=NaN;
if any(~isfinite(S))||any(S<=0), return; end
p=polyfit(TSL(:),log(S(:)),1); if p(1)>=0, return; end
T=-1/p(1); y=log(S(:)); yf=polyval(p,TSL(:));
ss=sum((y-yf).^2); st=sum((y-mean(y)).^2); if st>0, R2=1-ss/st; end
end
