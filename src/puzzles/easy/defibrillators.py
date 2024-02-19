import math

def deg2rad(x):
    return float(x.replace(',','.'))*(math.pi/180)

lon = deg2rad(input())
lat = deg2rad(input())
n = int(input())
bestName = ""
bestDist = float("inf")
for i in range(n):
    defib = input().split(";")
    defibLon = deg2rad(defib[4])
    defibLat = deg2rad(defib[5])
    x = (defibLon - lon) * math.cos((defibLat + lat)/2)
    y = defibLat - lat
    d = math.sqrt(x**2 + y**2)
    if (d < bestDist):
        bestDist = d
        bestName = defib[1]

print(bestName)
