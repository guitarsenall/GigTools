
'''
reorder_repertoire.py
'''

import gigtools as gt
repertwaar  = gt.read_repertwaar()
gig_songs   = gt.read_gig_songs(repertwaar, SongFile='last_gig_1.txt')

print( str(len(gig_songs)) + ' songs found:')

import math
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


