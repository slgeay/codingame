n, m = [int(i) for i in input().split()]
s ="".join([input() for i in range(n)])

rules = []
nextRule = 'Z'

while True:
    lastChar = s[0]
    lastPair = ""
    count = {}

    for char in s[1:]:
        pair = lastChar + char
        if pair == lastPair:
            lastPair = ""
        else:
            count[pair] = (count.get(pair) or 0) + 1
            lastPair = pair
        lastChar = char

    bestPair = ""
    bestCount = 1
    for pair in count:
        if count[pair] > bestCount:
            bestPair = pair
            bestCount = count[pair]

    if bestPair == "":
        break

    s = s.replace(bestPair, nextRule)
    rules.append(nextRule + " = " + bestPair)
    nextRule = chr(ord(nextRule) - 1)
    
print(s)
[print(rule) for rule in rules]