I,L=int,input
M=lambda _:map(I,L().split())
_,W,_,F,X,_,_,E=M(0)
e={F:X,**dict(map(M,[0]*E))}
while 1:f,p,r=L().split();f,p,r=I(f),I(p),r>"R";print("BWLAOICTK"[f<0 or p==e[f]or(p>e[f])^r::2])
