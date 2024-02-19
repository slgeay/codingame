a=s=""
for c in input():
 for b in f"{ord(c):07b}":s+=("0",(" 00 0"," 0 0")[b>"0"])[b!=a];a=b
print(s[1:])
