
'''
reverse_songlist.py

read, reverse, and print a list of songs in a file
specified at the command line.
'''

# detect a partial match and return score
def match_score(title, line):
    match   = 0
    for i in range( min(len(title),len(line)) - 1 ):
        if line[i:i+2] in title:
            match += 1
    return match / (len(title)-1) * 100


import sys
#print ('argument list', sys.argv)
FileName = sys.argv[1]

#file = open(FileName)
#lines = []
#for line in file.readlines():
#    # strip the return from each line
#    line = line.replace('\n', '')
#    lines.append(line)
#file.close()
#songs = lines
#songs.reverse()
#print(*songs, sep='\n')

# read the Repertwaar CSV file into repertwaar, a list of dictionaries
import csv
import math
repertwaar   = []    # a list of dictionaries
with open('music_performance_repertoire.csv', 'r') as file:
    csvreader = csv.DictReader(file, quotechar='"', delimiter=',',
                                quoting=csv.QUOTE_ALL )
    for row in csvreader:
        #print( row['song'], float(row['energy']) )
        title   = row['song']
        energy  = float(row['energy'])
        song    = { 'title'     : row['song']           ,
                    'energy'    : float(row['energy'])  ,
                    'data'      : row                   }
        repertwaar.append(song)
gig_songs   = []
ScoreThreshold  = 70.0
SqrEnergy       = 0.0
with open(FileName, 'r') as file:
    lines = []
    for line in file.readlines():
        lines.append(line.strip())  # strip the return
        ThisSong    = repertwaar[0]
        ThisScore   = 0.0
        LastScore   = 0.0
        for song in repertwaar:
            score   = match_score( song['title'], line.strip() )
            if score >= ThisScore:
                LastSong    = ThisSong
                LastScore   = ThisScore
                ThisSong    = song
                ThisScore   = score
        #print( line.strip(), ';', ThisSong['title'], ';', ThisScore, ';',
        #        LastScore,   ';', LastSong['title'],  )
        if ThisScore >= ScoreThreshold:
            SqrEnergy   = SqrEnergy + ThisSong['energy']**2
            gig_songs.append(ThisSong)
        else:
            print('Unmatched line: ' + line.strip() )
GigRMSEnergy    = math.sqrt( SqrEnergy / len(gig_songs) )
print('Gig Energy Index = ' + str(GigRMSEnergy))
print( str(len(gig_songs)) + ' songs found:')
gig_songs.reverse()
for song in gig_songs:
    print(song['title'].removesuffix('*'))

