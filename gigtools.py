#   gigtools.py
''' A set of functions for analyzing gig data '''

import docx
import os
import unicodedata
import datetime


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
                        'playdates' : []                    ,
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


def read_gig_files(gig_files, repertwaar, verbose=False):
    ''' read a list of .docx files, modify the contents of repertwaar,
        and return a list of gigs. '''
    gigs    = []
    ScoreThreshold  = 70.0
    for GigFile in gig_files:
        doc = docx.Document(GigFile)
        allText = []
        for docpara in doc.paragraphs:
            allText.append(unicodedata.normalize('NFKD',docpara.text))
        # find the title lines
        title_idx   = []
        for i, line in enumerate(allText):
            if 'Performance #' in line:
                #print(f'Found one at {i}: {line}')
                b   = 0
                for b in range(10):
                    if i-b < 0:
                        print(f'Missing title for line {i}: {line}')
                        break
                    if '/24' in allText[i-b]:
                        title_idx.append(i-b)
                        #print(f'\tTitle: {allText[i-b]}')
                        break
        if verbose:
            print(f'Found {len(title_idx)} gig titles in {GigFile}:')
            for i in title_idx:
                print('\t' + allText[i])
        title_idx.append(len(allText)-1)
        # loop over the gig sections
        for i in range(len(title_idx)-1):
            gig_lines   = allText[ title_idx[i] : title_idx[i+1]-1 ]
            title       = allText[title_idx[i]]
            if verbose:
                print(f'Parsing Gig title: {title}')
            # get the venue and date
            tok         = title.rpartition(' ')
            venue       = tok[0]
            datestr     = tok[2]
            m,d,y       = datestr.split('/')
            gigdate     = datetime.date( int(y)+2000, int(m), int(d) )
            # get the song list
            blocks      = []
            song_list   = []
            this_block  = []
            for line in gig_lines:
                if line == ' ':
                    blocks.append(this_block[:])    # copy the list
                    this_block  = []
                else:
                    this_block.append(line)
            for block in blocks:
                if len(block) >= 9:
                    matches = 0
                    for line in block:
                        score   = score_line(repertwaar, line)
                        if score >= ScoreThreshold:
                            # increment the match count
                            matches += 1
                    if matches / len(block) >= 0.50:
                        # song list found
                        song_list   = block
                        break
            gig_songs   = match_gig_songs(repertwaar, song_list)
            if verbose:
                print(f'\t{len(gig_songs)} songs found' )
                print(f'\t{len(gig_lines)} text lines' )
            for song in gig_songs:
                song['playcount']  += 1
                song['playdates'].append(gigdate)
            gig = { 'Title' : allText[title_idx[i]] ,
                    'Venue' : venue                 ,
                    'Date'  : gigdate               ,
                    'Songs' : gig_songs             ,
                    'Lines' : gig_lines             }
            gigs.append(gig)
    return gigs


def gigs_by_venue(gigs):
    ''' Accepts a list of gigs, output is a dictionary where each
        element is a list of gigs for that venue.'''
    gigs_copy       = gigs[:]
    venue_gigs  = {}
    while gigs_copy:                             # not empty
        gig                 = gigs_copy.pop()
        VName               = gig['Venue'].strip().title()
        venue_gigs[VName]   = [gig]
        print(f'Got the first {VName}. Searching for more.')
        #   find & remove all matches
        c           = 0
        searching   = True
        while searching:
            for j in range(len(gigs_copy)):
                # compare gig['Venue'] with VName
                gig = gigs_copy[j]
                s   = match_score( VName, gig['Venue'].strip().title() )
                if s >= 60:
                    print(f'\t\tFound another {VName}. Popping...')
                    venue_gigs[VName].append( gigs_copy.pop(j) )
                    break                   # for loop
            if len(gigs_copy)==0 or len(gigs_copy)<c:
                searching   = False
                print(f'\tfor loop done with {VName}')
                print(f'\tNumber of gigs left = {len(gigs_copy)}')
            c   += 1
    return venue_gigs

