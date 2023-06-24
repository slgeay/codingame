n=int(input())
p=2
while p<n and n%p:p+=1
print([p,"NONE"][p>n])
