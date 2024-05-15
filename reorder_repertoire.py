
'''
reorder_repertoire.py
'''


# detect a partial match and return score
def match_score(title, line):
    match   = 0
    for i in range( min(len(title),len(line)) - 1 ):
        if line[i:i+2] in title:
            match += 1
    return match / (len(title)-1) * 100


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

# read the songs from the last gig in last_gig_1.txt
# The name indicates I might want to include more than one
# previous gig.
gig_songs   = []
ScoreThreshold  = 70.0
with open('last_gig_1.txt', 'r') as file:
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
            gig_songs.append(ThisSong)
        else:
            print('Unmatched line: ' + line.strip() )
print( str(len(gig_songs)) + ' songs found:')
#gig_songs.reverse()
SqrEnergy   = 0.0
for song in gig_songs:
    SqrEnergy   = SqrEnergy + song['energy']**2
    #print(song['title'].removesuffix('*'))
GigRMSEnergy    = math.sqrt( SqrEnergy / len(gig_songs) )
print('Gig Energy Index = ' + str(GigRMSEnergy))

'''
Reorder the Repertwaar based on last gig:
move songs from last gig (last_gig_1.txt) to bottom of the Repertwaar to
create a prioritized list that deprioritizes most recently played at a
given venue.
'''
# sort the Repertwaar by title
repertwaar.sort( key = lambda s: s['title'] )
for RepSong in repertwaar:
    if RepSong not in gig_songs:
        print(RepSong['title'].removesuffix('*'))
print('####################')
for song in gig_songs:
    print(song['title'].removesuffix('*'))


