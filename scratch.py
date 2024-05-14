
'''
scratch.py
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
songs   = []
ScoreThreshold  = 70.0
with open('songlist.txt', 'r') as file:
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
            songs.append(ThisSong)
        else:
            print('Unmatched line: ' + line.strip() )
print( str(len(songs)) + ' songs found:')
songs.reverse()
for song in songs:
    print(song['title'].removesuffix('*'))


## detect a partial match
#title   = "Wild World"
#line    = "Wild World"
#match   = 0
#for i in range( min(len(title),len(line)) - 1 ):
#    if line[i:i+2] in title:
#        print( line[i:i+2] )
#        match += 1
#score   = match / (len(title)-1) * 100


## read, reverse, and print a list of songs in a file
#file = open('songlist.txt')
#lines = []
#for line in file.readlines():
#    line = line.replace('\n', '')
#    lines.append(line)
#file.close()
#songs = lines
#songs.reverse()
#print(*songs, sep='\n')


## print a simple list of songs
#songs   = [
#            "The Mission"                    ,
#            "Under The Sun"                  ,
#            "Emmaus"                         ,
#            "As Warm As Tears"               ,
#            "Those Who Wait"                 ,
#            "Del's Bells"                    ,
#            "Nothing But The Call"           ,
#            "Time In A Bottle"               ,
#            "Still The One"                  ,
#            "The Wind & The Wheat"           ,
#            "You've Got A Friend"            ,
#            "Solitary Man"                   ,
#            "Misunderstanding"               ,
#            "If You Could Read My Mind"      ,
#            "Here, There and Everywhere"     ,
#            "Crazy Little Thing Called Love" ,
#            "Even The Losers"                ,
#            "Shilo"                          ,
#            "Kashmir"                        ,
#            "Metamorphosis"                  ,
#            "Classical Gas"                  ,
#            "Doctor My Eyes"                 ,
#            "Behind Blue Eyes"               ,
#            "Addison's Walk"                 ,
#            "Beginnings"                     ,
#            "Sailing"                        ,
#            "Blackbird"                      ,
#            "Everything I Own"               ,
#            "Infinite Horizon / County Down" ,
#            "The Reunion"                    ,
#            "Wild World"                     ,
#            "Here Comes The Sun"             ,
#            "Time After Time"                ,
#            "Something"                      ,
#            "I've Got A Name"                ]
#songs.reverse()
#print(*songs, sep='\n')

