# Migrate from Bronze weights to Silver weights
import os

def add_zeros(w):
    i = 8
    while i <= len(w):
        w[i:i] = [0.0, 0.0]
        i += 10  # Move 10 steps ahead, 8 steps for original floats and 2 steps for added zeros
    return w


def process_content(s):
    w = [float(i) for i in s.split(",")]
    w = add_zeros(w)
    return ",".join([str(i) for i in w])

def migrate_directory(directory):
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)
        if os.path.isfile(filepath):
            with open(filepath, 'r') as file:
                s = file.read()
            s = process_content(s)
            with open(filepath, 'w') as file:
                file.write(s)
