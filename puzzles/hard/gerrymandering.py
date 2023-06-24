W, H = [int(i) for i in input().split()]
voters = [[] for _ in range(H)]

for h in range(H):
    for w, data in enumerate(input().split()):
        voters[h].append(
            max(
                [int(data)]
                + [voters[h][wc] + voters[h][w - wc - 1] for wc in range((w + 1) // 2)]
                + [voters[hc][w] + voters[h - hc - 1][w] for hc in range((h + 1) // 2)]
            )
        )

print(voters[H - 1][W - 1])
