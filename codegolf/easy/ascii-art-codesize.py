i=input
L,H,T=int(i()),int(i()),i()
exec('l=i();print("".join([l[L*([26,ord(c)-65]["@"<c<"["]):][:L]for c in T.upper()]));'*H)
