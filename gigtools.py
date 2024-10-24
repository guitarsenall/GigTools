#   gigtools.py
''' A set of functions for analyzing gig data '''

import docx
import os
import unicodedata
import datetime


def fix_venue_name(VName):
    ''' removes the apostrophe from a venue name '''
    return ''.join( ch for ch in VName if ch.isascii() )


def match_score(title, line):
    ''' detect a partial match and return score '''
    title   = title.strip().removesuffix('*')
    line    = line.strip().removesuffix('*')
    if '(' in line:
        # remove venue-play markings
        tok     = line.rpartition('(')
        line    = tok[0].strip()
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
            song    = { 'title'         : row['song']           ,
                        'energy'        : float(row['energy'])  ,
                        'guitar_1st'    : row['guitar_1st']     ,
                        'guitar_2nd'    : row['guitar_2nd']     ,
                        'mastery'       : float(row['mastery']) ,
                        'playcount'     : 0                     ,
                        'playdates'     : []                    ,
                        'data'          : row                   }
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
            title       = allText[ title_idx[i] ]
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
            guitars     = []
            mileage     = 0.0
            for line in gig_lines:
                if line == ' ':
                    blocks.append(this_block[:])    # copy the list
                    this_block  = []
                else:
                    this_block.append(line)
                    if 'guitars:' in line.lower():
                        GuitarStr   = line.removeprefix('Guitars:')
                        for tok in GuitarStr.split(','):
                            guitars.append( tok.strip() )
                        guitars.sort()
                    if 'mileage:' in line.lower():
                        # might be form '75*2 = 150'
                        MileStr = line.removeprefix('Mileage:')
                        tok     = MileStr.split(' ')
                        mileage = float( tok[-1] )
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
            gig = { 'title'     : allText[title_idx[i]] ,
                    'venue'     : fix_venue_name(venue) ,
                    'date'      : gigdate               ,
                    'mileage'   : mileage               ,
                    'guitars'   : guitars               ,
                    'songs'     : gig_songs             ,
                    'lines'     : gig_lines             }
            gigs.append(gig)
    return gigs


def gigs_by_venue(gigs, verbose=False):
    ''' Accepts a list of gigs, output is a dictionary where each
        element is a list of gigs for that venue.'''
    gigs_copy       = gigs[:]
    venue_gigs  = {}
    while gigs_copy:                             # not empty
        gig                 = gigs_copy.pop()
        VName               = gig['venue'].strip().lower()
        venue_gigs[VName]   = [gig]
        if verbose:
            print(f'Got the first {VName}. Searching for more.')
        #   find & remove all matches
        c           = 0
        searching   = True
        while searching:
            for j in range(len(gigs_copy)):
                # compare gig['venue'] with VName
                gig = gigs_copy[j]
                s   = match_score( VName, gig['venue'].strip().lower() )
                if s >= 60:
                    if verbose:
                        print(f'\t\tFound another {VName}. Popping...')
                    venue_gigs[VName].append( gigs_copy.pop(j) )
                    break                   # for loop
            if len(gigs_copy)==0 or len(gigs_copy)<c:
                searching   = False
                if verbose:
                    print(f'\tfor loop done with {VName}')
                    print(f'\tNumber of gigs left = {len(gigs_copy)}')
            c   += 1
    return venue_gigs


def venue_play_list(VenueName, gigs, repertwaar):
    ''' prints the repertwaar titles with markings from previous
        gigs at VenueName'''
    venue_gigs      = gigs_by_venue(gigs)
    print('gigs found per venue:')
    for k, v in venue_gigs.items():
        print(f'\t{k}: {len(v)}')
    print('all venue names:')
    for gig in gigs:
        print( '\t' + gig['venue'].strip().title() )
    v_gigs      = venue_gigs[VenueName.lower()]
    v_gigs.sort( key = lambda g: g['date'], reverse=True )
    for gig in v_gigs:
        print(f"gig date: {gig['date']}")
    print('')

    # add PlayString suffixes to songs played at this venue
    for song in repertwaar:
        SongName    = song['title'].removesuffix('*')
        PlayString  = ' ('
        played      = False
        for i, gig in enumerate(v_gigs):
            if i > 9:
                break
            # get song titles
            gig_song_titles = []
            for s in gig['songs']:
                gig_song_titles.append(s['title'].removesuffix('*'))
            if SongName in gig_song_titles:
            # if 'this song is in this gig':
                played      = True
                PlayString  += str(i+1)
        if played:
            PlayString += ')'
        else:
            PlayString = ''
        TitleString = SongName + PlayString
        print(TitleString)


def guitar_report(gigs, verbose=False):
    ''' Reads number of gigs and songs performed since last string change '''
    # Read data from guitars.txt into guitars, a dictionary list
    with open('guitars.txt', 'r') as file:
        lines = file.readlines()
    # find the guitar lines
    guitar_idx      = []
    guitar_names    = []
    for i, line in enumerate(lines):
        tok = line.split(':')
        if len(tok) > 1 and 'guitar' in tok[0].lower():
            guitar_idx.append(i)
            guitar_names.append(tok[1].strip())
    if verbose:
        print(f'Found {len(guitar_idx)} guitars in guitars.txt:')
        for i in guitar_idx:
            print('\t' + lines[i].strip())
    guitar_idx.append(len(lines)-1)   # last line
    # loop over the guitar sections
    guitars  = []
    for i in range(len(guitar_idx)-1):
        guitar_lines    = lines[ guitar_idx[i] : guitar_idx[i+1] ]
        title           = lines[ guitar_idx[i] ]
        if verbose:
            print(f'Parsing guitar line: {title.strip()}')
        GuitarType  = ''
        for line in guitar_lines:
            tok = line.split(':')
            if len(tok) > 1 and 'type' in tok[0].lower():
                GuitarType  = tok[1].strip()
            if len(tok) > 1 and 'strings' in tok[0].lower():
                datestr = tok[1]
                m,d,y   = datestr.split('/')
                StringDate  = datetime.date( int(y)+2000, int(m), int(d) )
        guitar  = { 'name'      : guitar_names[i]   ,
                    'type'      : GuitarType        ,
                    'change'    : StringDate        ,
                    'all lines' : guitar_lines      }
        guitars.append(guitar)
        if verbose:
            print(f"\tname  : {guitar_names[i]}")
            print(f"\ttype  : {GuitarType}")
            print(f"\tchange : {StringDate}")
    # track guitars used in gigs since a given date
    gigs.sort( key = lambda g: g['date'], reverse=False )
    for guitar in guitars:
        if verbose:
            print(f"Guitar: {guitar['name']}")
        SinceDate   = guitar['change']
        GigCount    = 0
        SongCount   = 0
        for gig in gigs:
            if gig['date'] >= SinceDate and guitar['name'] in gig['guitars']:
                GigCount   += 1
                if verbose:
                    print( "\t{0:<12}: {1:<40}: {2}".format(
                            str(gig['date']), gig['venue'], gig['guitars'] ) )
                for song in gig['songs']:
                    if song['data']['guitar_1st'] == guitar['type']:
                        SongCount   += 1
                        if verbose:
                            print(f"\t\t{song['title']}")
        if verbose:
            print(f"{guitar['name']}: {GigCount} gigs, {SongCount} songs' "
                    + "since string change\n")
        else:
            print("{0:<10}:{1:>8}:{2:>10}".format(
                    guitar['name']              ,
                    str(GigCount) + ' gigs'     ,
                    str(SongCount) + ' songs'   ) )


def mileage_report(gigs, BegDate, EndDate):
    print( f"Mileage report {BegDate} to {EndDate}:" )
    print( "{0:<40}|{1:>10}|{2:>7}|{3:>5}|".format(
                'venue', 'mileage', '# gigs', 'sum' ) )
    print( "{0:<40}|{1:>10}|{2:>7}|{3:>5}|".format(
                '-'*40, '-'*10, '-'*7, '-'*5 ) )
        # sum: {3:4.0f}
    venue_gigs  = gigs_by_venue(gigs)
    TotalGigs   = 0
    TotalMiles  = 0.0
    venue_names = sorted( venue_gigs.keys() )
    for VName in venue_names:
        v_gigs      = venue_gigs[VName]
        VenueName   = v_gigs[0]['venue']
        GigMileage  = v_gigs[0]['mileage']
        NGigs       = 0
        for gig in v_gigs:
            if gig['date'] >= BegDate and gig['date'] <= EndDate:
                NGigs   += 1
        TotalGigs   += NGigs
        TotalMiles  += NGigs*GigMileage
        print( "{0:<40}|{1:10.1f}|{2:7d}|{3:5.0f}|".format(
                    VenueName           ,
                    GigMileage          ,
                    NGigs               ,
                    NGigs*GigMileage    ) )
    print( "{0:<40}|{1:>10}|{2:>7}|{3:>5}|".format(
                '-'*40, '-'*10, '-'*7, '-'*5 ) )
    print( "{0:<40}|{1:>10}|{2:7d}|{3:5.0f}|".format(
                'TOTAL'             ,
                ''                  ,
                TotalGigs           ,
                TotalMiles          ) )


def play_count(gigs, RehearsalFile, repertwaar):
    ''' print songs with play intervals and freshness score'''
    #
    #   read Rehearsals
    #
    with open(RehearsalFile, 'r') as file:
        lines = file.readlines()
    # find the date lines
    date_idx        = []
    rehearse_dates  = []
    for i, line in enumerate(lines):
        tok = line.split(':')
        if len(tok) > 1 and 'date' in tok[0].lower():
            date_idx.append(i)
            datestr = tok[1]
            m,d,y   = datestr.split('/')
            RDate   = datetime.date( int(y)+2000, int(m), int(d) )
            rehearse_dates.append(RDate)
    print(f'Found {len(date_idx)} dates in rehearsal.txt:')
    for i in date_idx:
        print('\t' + lines[i].strip())
    date_idx.append(len(lines)-1)   # last line
    # loop over the rehearsal sections
    rehearsals  = []
    for i in range(len(date_idx)-1):
        reh_lines   = lines[ date_idx[i] : date_idx[i+1] ]
        title       = lines[ date_idx[i] ]
        print(f'Parsing Rehearsal Date: {title}')
        # get the song list
        blocks      = []
        this_block  = []
        for line in reh_lines:
            if line.strip() == '':
                blocks.append(this_block[:])    # copy the list
                this_block  = []
            else:
                this_block.append(line)
        blocks.append(this_block[:])    # last block
        BestBlock   = blocks[0]
        BestMatches = 0
        for block in blocks:
            matches = 0
            for line in block:
                score   = score_line(repertwaar, line.strip())
                if score >= 70.0:
                    # increment the match count
                    matches += 1
            if matches > BestMatches:
                # song list might be found
                BestBlock   = block
                BestMatches = matches
                break
        reh_songs   = match_gig_songs(repertwaar, BestBlock)
        print(f'\t{len(reh_songs)} songs found' )
        print(f'\t{len(reh_lines)} text lines' )
        for song in reh_songs:
            song['playcount']  += 1
            song['playdates'].append(rehearse_dates[i])
        rehearsal   = { 'Date'  : rehearse_dates[i]     ,
                        'Songs' : reh_songs             ,
                        'Lines' : reh_lines             }
        rehearsals.append(rehearsal)
    #
    #   compute Freshness
    #
    CurDate     = datetime.date.today()
    for song in repertwaar:
        #song        = repertwaar[63]
        tau         = song['mastery']
        if song['playcount'] > 0:
            gig_dates   = sorted( song['playdates'], reverse=False )
            ThisDate    = gig_dates[0] + datetime.timedelta(days=1)
            dF          = 0.0
            F           = 1.0
            DayNum      = 1
            while ThisDate <= CurDate:
                if DayNum   >= 1000:
                    raise RuntimeError('Reached 1000 days')
                    break
                P = 1 if ThisDate in song['playdates'] else 0
                dF  = ( P - F/tau ) / tau
                F   = ( F/tau + dF ) * tau
                #print( '{0:3d}: {1:3d} {2:5.3f}, {3:4.2f}'.format(DayNum, P, dF, F ) )
                DayNum      += 1
                ThisDate    += datetime.timedelta(days=1)
            song['freshness']   = F
        else:
            song['freshness']   = 0.0
    #
    #   analysis and printout
    #
    repertwaar.sort( key = lambda s: s['freshness'], reverse=False )
    print('song freshness and play intervals:')
    for song in repertwaar:
        if song['playcount'] > 0:
            # form the play-interval string
            gig_dates   = sorted( song['playdates'], reverse=True )
            CurDate     = datetime.date.today()
            delta       = CurDate - gig_dates[0]
            DeltaString = f'{delta.days}'
            CurDate     = gig_dates[0]
            for gigdate in gig_dates[1:]:
                delta       = CurDate - gigdate
                DeltaString += f',{delta.days}'
                CurDate     = gigdate
        else:
            DeltaString = ''
        print( '\t{0:<40} ({1:2d}, {2:3d}%): {3}'.format(
                    song['title'].removesuffix('*'),
                    int(song['mastery']),
                    int(100*song['freshness']),
                    DeltaString ) )

