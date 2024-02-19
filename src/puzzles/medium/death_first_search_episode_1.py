n, l, e = [int(i) for i in input().split()]
links = [set() for node in range(n)]
exits = set()

for i in range(l):
    n1, n2 = [int(j) for j in input().split()]
    links[n1].add(n2)
    links[n2].add(n1)

for i in range(e):
    exits.add(int(input()))

def pathToNearestExit(a):
    visited = [False for node in range(n)]
    q = [a]
    path = {a: []}

    while len(q):
        node = q.pop(0)
        if node in exits:
            return path[node]

        for neighbor in links[node]:
            if neighbor not in path:
                path[neighbor] = path[node] + [neighbor]
                q.append(neighbor)


# game loop
while True:
    si = int(input())
    path = [si]+pathToNearestExit(si)
    i = 1 if len(path) > 2 else 0
    a,b = path[i],path[i+1]
    print(a, b)
    links[a].remove(b)
    links[b].remove(a)
