I,L=int,input
M=lambda _:map(I,L().split())
_,W,_,F,X,_,_,E=M(0)
e=dict(map(M,[0]*E))
while 1:f,p,r=L().split();f,p,r=I(f),I(p),r>"R";x=[e.get(f,[0,W-1][r]),X][f==F];print("BWLAOICTK"[(f<0)|(p==x)|r^(p>x)::2])

