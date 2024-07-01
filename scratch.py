
'''
scratch.py
'''

import gigtools as gt
import datetime


## oil change
#OldDate     = datetime.date( 2023, 12, 29 )      # YYYY, MM, DD
#OldMiles    = 172617.0
#NewDate     = datetime.date( 2024,  6, 19 )      # YYYY, MM, DD
#NewMiles    = 175823.0
#delta       = NewDate - OldDate
#DeltaString = f'{delta.days}'
#mpd         = (NewMiles-OldMiles) / delta.days
#NextDate    = NewDate + datetime.timedelta(days = 3000.0/mpd)
#print(f'Miles per day = {mpd}')
#print(f'Next change on {NextDate}')


# read in the repertwaar--a list of song dictionaries
repertwaar      = gt.read_repertwaar()
repertwaar.sort( key = lambda s: s['title'] )

# read the gig history
GigFolder       = 'S:\\will\\documents\\OneDrive\\2024\\gigtools\\gigfiles\\'
GigFile         = 'multi.docx'
gig_files       = [ GigFolder + 'gigs_january_2024.docx'    ,
                    GigFolder + 'gigs_february_2024.docx'   ,
                    GigFolder + 'gigs_march_2024.docx'      ,
                    GigFolder + 'gigs_april_2024.docx'      ,
                    GigFolder + 'gigs_may_2024.docx'        ,
                    GigFolder + 'gigs_june_2024.docx'       ]
gigs            = gt.read_gig_files( gig_files, repertwaar, verbose=True)


## Read data from guitars.txt into guitars, a dictionary list
#with open('guitars.txt', 'r') as file:
#    lines = file.readlines()
## find the guitar lines
#guitar_idx      = []
#guitar_names    = []
#for i, line in enumerate(lines):
#    tok = line.split(':')
#    if len(tok) > 1 and 'guitar' in tok[0].lower():
#        guitar_idx.append(i)
#        guitar_names.append(tok[1].strip())
#print(f'Found {len(guitar_idx)} guitars in guitars.txt:')
#for i in guitar_idx:
#    print('\t' + lines[i].strip())
#guitar_idx.append(len(lines)-1)   # last line
## loop over the guitar sections
#guitars  = []
#for i in range(len(guitar_idx)-1):
#    guitar_lines    = lines[ guitar_idx[i] : guitar_idx[i+1] ]
#    title           = lines[ guitar_idx[i] ]
#    print(f'Parsing guitar line: {title.strip()}')
#    GuitarType  = ''
#    for line in guitar_lines:
#        tok = line.split(':')
#        if len(tok) > 1 and 'type' in tok[0].lower():
#            GuitarType  = tok[1].strip()
#        if len(tok) > 1 and 'strings' in tok[0].lower():
#            datestr = tok[1]
#            m,d,y   = datestr.split('/')
#            StringDate  = datetime.date( int(y)+2000, int(m), int(d) )
#    guitar  = { 'name'      : guitar_names[i]   ,
#                'type'      : GuitarType        ,
#                'change'    : StringDate        ,
#                'all lines' : guitar_lines      }
#    guitars.append(guitar)
#    print(f"\tname  : {guitar_names[i]}")
#    print(f"\ttype  : {GuitarType}")
#    print(f"\tchange : {StringDate}")
#
## track guitars used in gigs since a given date
#gigs.sort( key = lambda g: g['date'], reverse=False )
#for guitar in guitars:
#    print(f"Guitar: {guitar['name']}")
#    SinceDate   = guitar['change']
#    GigCount    = 0
#    SongCount   = 0
#    for gig in gigs:
#        if gig['date'] >= SinceDate and guitar['name'] in gig['guitars']:
#            GigCount   += 1
#            print( "\t{0:<12}: {1:<40}: {2}".format(
#                    str(gig['date']), gig['venue'], gig['guitars'] ) )
#            for song in gig['songs']:
#                if song['data']['guitar'] == guitar['type']:
#                    SongCount   += 1
#                    print(f"\t\t{song['title']}")
#    print(f"{GigCount} gigs, {SongCount} songs, since string change\n")



## Print all gigs with their energies
#import math
#def gig_energy(gig, verbose=False):
#    SqrEnergy   = 0.0
#    for song in gig['songs']:
#        SqrEnergy   = SqrEnergy + song['energy']**2
#    GigRMSEnergy    = math.sqrt( SqrEnergy / len(gig['songs']) )
#    gig['energy']   = GigRMSEnergy
#    if verbose:
#        print("{0:<40}: {1:3.1f}".format(
#                        gig['title'], gig['energy'] ))
#        for song in gig['songs']:
#            print("\t{0:<40}: {1:3.1f}".format(
#                        song['title'], song['energy'] ))
#    return gig['energy']
#for i,gig in enumerate(gigs):
#    GigEnergy   = gig_energy(gig, verbose=False)
#    print("{0:3d}: {1:<40}: {2:3.1f}".format( i,
#                        gig['title'], gig['energy'] ))



## track guitars used in gigs since a given date
#SinceDate   = datetime.date( 2024, 5, 29 )      # YYYY, MM, DD
#gigs.sort( key = lambda g: g['date'], reverse=False )
#for gig in gigs:
#    if gig['date'] >= SinceDate:
#        print( "\t{0:<12}: {1:<40}: {2}".format(
#                str(gig['date']), gig['venue'], gig['guitars'] ) )


## track plays in venue
#VenueName   = "Independence Village"
#gt.venue_play_list(VenueName, gigs, repertwaar)


## play with arranging list
#import random
#g   = [0, 4, 1, 5, 2, 4, 3, 4, 5, 2, 6, 4, 7, 2, 8]
##for i in range(200):
##    g.append( random.randint(0,20) )
#v   = {}
#gcopy   = g[:]
#print(f'g = {g}')
#while g:                                # g not empty
#    i   = g.pop()
#    v[i]    = []
#    v[i].append(i)
#    print(f'Got the first {i}. g = {g}')
#    #   find & remove all matches
#    c   = 0
#    searching   = True
#    while searching:
#        print(f'searching for {i}')
#        for j in range(len(g)):
#            if g[j]==i:
#                print(f'\t\tFound another {i}. Popping...')
#                v[i].append( g.pop(j) )
#                print(f'\t\tg = {g}')
#                break                   # for loop
#        if len(g)==0 or len(g)<c:
#            searching   = False
#            print(f'\tfor loop done with {i}')
#            print(f'\tg = {g}')
#        c   += 1



## sort repertwaar on most recent playdate, and display
#played_songs    = []
## get the earliest date
#MinDate         = datetime.date.today()
#for song in repertwaar:
#    if song['playcount'] > 0:
#        played_songs.append(song)
#        MinDate = min( MinDate, min(song['playdates']) )
## write earliest date to unplayed songs
#for song in repertwaar:
#    if song['playcount'] == 0:
#        song['playdates'].append(MinDate)
## sort the repertwaar
#repertwaar.sort( key = lambda s: max(s['playdates']) )
## analysis and printout
#print('play counts by song:')
#for song in repertwaar:
#    if song['playcount'] > 0:
#        # form the play-interval string
#        gig_dates   = sorted( song['playdates'], reverse=True )
#        CurDate     = datetime.date.today()
#        delta       = CurDate - gig_dates[0]
#        DeltaString = f'{delta.days}'
#        CurDate     = gig_dates[0]
#        for gigdate in gig_dates[1:]:
#            delta       = CurDate - gigdate
#            DeltaString += f',{delta.days}'
#            CurDate     = gigdate
#    else:
#        DeltaString = ''
#    print( '\t{0:<40}: {1:3d} plays : {2}'.format(
#                song['title'].removesuffix('*'),
#                song['playcount'], DeltaString ) )



## read rehearsals.txt
#repertwaar      = gt.read_repertwaar()
#with open('rehearsals.txt', 'r') as file:
#    lines = file.readlines()
## find the date lines
#date_idx        = []
#rehearse_dates  = []
#for i, line in enumerate(lines):
#    tok = line.split(':')
#    if len(tok) > 1 and 'date' in tok[0].lower():
#        date_idx.append(i)
#        datestr = tok[1]
#        m,d,y   = datestr.split('/')
#        RDate   = datetime.date( int(y)+2000, int(m), int(d) )
#        rehearse_dates.append(RDate)
#print(f'Found {len(date_idx)} dates in rehearsal.txt:')
#for i in date_idx:
#    print('\t' + lines[i].strip())
#date_idx.append(len(lines)-1)   # last line
## loop over the rehearsal sections
#rehearsals  = []
#for i in range(len(date_idx)-1):
#    reh_lines   = lines[ date_idx[i] : date_idx[i+1]-1 ]
#    title       = lines[ date_idx[i] ]
#    print(f'Parsing Rehearsal Date: {title}')
#    # get the song list
#    blocks      = []
#    this_block  = []
#    for line in reh_lines:
#        if line.strip() == '':
#            blocks.append(this_block[:])    # copy the list
#            this_block  = []
#        else:
#            this_block.append(line)
#    blocks.append(this_block[:])    # last block
#    BestBlock   = blocks[0]
#    BestMatches = 0
#    for block in blocks:
#        matches = 0
#        for line in block:
#            score   = gt.score_line(repertwaar, line.strip())
#            if score >= 70.0:
#                # increment the match count
#                matches += 1
#        if matches > BestMatches:
#            # song list might be found
#            BestBlock   = block
#            BestMatches = matches
#            break
#    reh_songs   = gt.match_gig_songs(repertwaar, BestBlock)
#    print(f'\t{len(reh_songs)} songs found' )
#    print(f'\t{len(reh_lines)} text lines' )
#    for song in reh_songs:
#        song['playcount']  += 1
#        song['playdates'].append(rehearse_dates[i])
#    rehearsal   = { 'Date'  : rehearse_dates[i]     ,
#                    'Songs' : reh_songs             ,
#                    'Lines' : reh_lines             }
#    rehearsals.append(rehearsal)


## get the venue and date from title
#title   = 'Germantown Spring Fling 5/4/24'
#tok     = title.rpartition(' ')
#venue   = tok[0]
#datestr = tok[2]
#m,d,y   = datestr.split('/')
#date    = dt.date( int(y)+2000, int(m), int(d) )
#diff    = dt.date.today() - date


## read a set of DOCX files containing multiple gigs using docx,
## and print play counts.
#repertwaar      = gt.read_repertwaar()
#GigFolder       = 'S:\\will\\documents\\OneDrive\\2024\\gigtools\\gigfiles\\'
#GigFile         = 'multi.docx'
#gig_files       = [ GigFolder + 'gigs_january_2024.docx'    ,
#                    GigFolder + 'gigs_february_2024.docx'   ,
#                    GigFolder + 'gigs_march_2024.docx'      ,
#                    GigFolder + 'gigs_april_2024.docx'      ,
#                    GigFolder + 'gigs_may_2024.docx'        ]
#gigs            = gt.read_gig_files(gig_files, repertwaar)
#played_songs    = []
#for song in repertwaar:
#    if song['playcount'] > 0:
#        played_songs.append(song)
#repertwaar.sort( reverse=True, key = lambda s: s['playcount'] )
#playcount   = 0
#print('play counts by song:')
#for song in repertwaar:
#    if song['playcount'] > 0:
#        # form the play-interval string
#        gig_dates   = sorted( song['playdates'], reverse=True )
#        CurDate     = dt.date.today()
#        delta       = CurDate - gig_dates[0]
#        DeltaString = f'{delta.days}'
#        CurDate     = gig_dates[0]
#        for gigdate in gig_dates[1:]:
#            delta       = CurDate - gigdate
#            DeltaString += f',{delta.days}'
#            CurDate     = gigdate
#    else:
#        DeltaString = ''
#    print( '\t{0:<40}: {1:d} plays : {2}'.format(
#                song['title'].removesuffix('*'),
#                song['playcount'], DeltaString ) )



## read a DOCX gig file using docx
#import docx
#import os
#import unicodedata
#ScoreThreshold  = 70.0
#repertwaar      = gt.read_repertwaar()
#GigFolder       = 'S:\\will\\documents\\OneDrive\\2024\\gigtools\\gigfiles\\'
#GigFile         = 'Tres Rojas 91023.docx'
#doc = docx.Document(GigFolder + GigFile)
#allText = []
#for docpara in doc.paragraphs:
#    allText.append(unicodedata.normalize('NFKD',docpara.text))
#blocks  = []
#this_block  = []
#for line in allText:
#    if line == ' ':
#        blocks.append(this_block[:])    # copy the list
#        this_block  = []
#    else:
#        this_block.append(line)
#for block in blocks:
#    if len(block) >= 5:
#        matches = 0
#        for line in block:
#            score   = gt.score_line(repertwaar, line)
#            if score >= ScoreThreshold:
#                # increment the match count
#                matches += 1
#        if matches / len(block) >= 0.50:
#            # song list found
#            song_list   = block
#            break
#gig_songs   = gt.match_gig_songs(repertwaar, song_list)
#for song in gig_songs:
#    song['playcount']  += 1
#for song in repertwaar:
#    print(song['title'].removesuffix('*'), ': ',
#            str(song['playcount']), ' plays' )


## read a PDF gig file using pypdf
#from pypdf import PdfReader
#import os
#os.chdir('S:\\will\\documents\\OneDrive\\2024\\gigtools')
#reader = PdfReader('gigfiles/Tres Rojas 91023.pdf')
#print(len(reader.pages))
#page = reader.pages[0]
#text = page.extract_text()
#print(text)


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

