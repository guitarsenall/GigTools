
'''
reverse_songlist.py

read, reverse, and print a list of songs in a file
specified at the command line.
'''

import sys
#print ('argument list', sys.argv)
FileName = sys.argv[1]

file = open(FileName)
lines = []
for line in file.readlines():
    # strip the return from each line
    line = line.replace('\n', '')
    lines.append(line)
file.close()
songs = lines
songs.reverse()
print(*songs, sep='\n')

