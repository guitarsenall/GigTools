
'''
reverse_songlist.py

read, reverse, and print a list of songs in a file
specified at the command line.
'''
import gigtools as gt
import sys

#print ('argument list', sys.argv)
FileName = sys.argv[1]

# read the Repertwaar CSV file into repertwaar, a list of dictionaries
repertwaar  = gt.read_repertwaar()

gig_songs   = gt.read_gig_songs(repertwaar, SongFile=FileName)

# calculate gig energy
import math
SqrEnergy   = 0.0
for song in gig_songs:
    SqrEnergy   = SqrEnergy + song['energy']**2
GigRMSEnergy    = math.sqrt( SqrEnergy / len(gig_songs) )
print('Gig Energy Index = ' + str(GigRMSEnergy))
print( str(len(gig_songs)) + ' songs found:')

# print the reversed song list
gig_songs.reverse()
for song in gig_songs:
    print(song['title'].removesuffix('*'))

