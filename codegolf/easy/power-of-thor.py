a,b,c,d=map(int,input().split())
x,y=a-c,b-d
V,H,x,y="EW"[x<0],"SN"[y<0],abs(x),abs(y)
[(input(),print(m))for m in[H+V]*min(x,y)+[V]*max(0,x-y)+[H]*max(0,y-x)]
