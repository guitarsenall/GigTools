#   gigtools.py


def match_score(title, line):
    ''' detect a partial match and return score '''
    title   = title.strip().removesuffix('*')
    line    = line.strip().removesuffix('*')
    match   = -abs( len(title) - len(line) )
    for i in range( min(len(title),len(line)) - 1 ):
        if line[i:i+2] in title:
            match += 1
    return match / (len(title)-1) * 100


def score_line(repertwaar, line):
    ''' find best match in repertwaar and return score '''
    ThisSong    = repertwaar[0]
    ThisScore   = 0.0
    LastScore   = 0.0
    for song in repertwaar:
        # use local version of match_score(), not gt
        score   = match_score( song['title'], line.strip() )
        if score >= ThisScore:
            LastSong    = ThisSong
            LastScore   = ThisScore
            ThisSong    = song
            ThisScore   = score
    return ThisScore


def read_repertwaar(CSVFile='music_performance_repertoire.csv'):
    ''' read the repertwaar from CSV file into a list of dictionaries '''
    import csv
    repertwaar   = []    # a list of dictionaries
    with open(CSVFile, 'r') as file:
        csvreader = csv.DictReader(file, quotechar='"', delimiter=',',
                                    quoting=csv.QUOTE_ALL )
        for row in csvreader:
            #print( row['song'], float(row['energy']) )
            title   = row['song']
            energy  = float(row['energy'])
            song    = { 'title'     : row['song']           ,
                        'energy'    : float(row['energy'])  ,
                        'playcount' : 0                     ,
                        'data'      : row                   }
            repertwaar.append(song)
    return repertwaar


def read_gig_songs(repertwaar, SongFile='songlist.txt'):
    ''' read the songs from the last gig in last_gig_1.txt
        The name indicates I might want to include more than one
        previous gig. '''
    gig_songs       = []
    ScoreThreshold  = 70.0
    with open(SongFile, 'r') as file:
        lines = []
        for line in file.readlines():
            # lines.append(line.strip())  # strip the return
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
    return gig_songs


def match_gig_songs(repertwaar, song_strings):
    ''' match the strings in song_strings with songs in repertwaar. '''
    gig_songs       = []
    ScoreThreshold  = 70.0
    for SongStr in song_strings:
        ThisSong    = repertwaar[0]
        ThisScore   = 0.0
        LastScore   = 0.0
        for song in repertwaar:
            score   = match_score( song['title'], SongStr.strip() )
            if score >= ThisScore:
                LastSong    = ThisSong
                LastScore   = ThisScore
                ThisSong    = song
                ThisScore   = score
        if ThisScore >= ScoreThreshold:
            gig_songs.append(ThisSong)
        else:
            print('Unmatched line: ' + SongStr.strip() )
    return gig_songs


