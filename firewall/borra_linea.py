#!/usr/bin/python
# coding = utf-8
import os
filename = 'test.txt'
with open(filename) as infile, open('output.txt', 'w') as outfile:
    for line in infile:
        if not line.strip(): continue  # skip the empty line
        outfile.write(line)  # non-empty line. Write it to output

os.remove('test.txt')
os.rename('output.txt','test.txt')
