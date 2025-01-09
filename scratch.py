
'''
scratch.py
'''

import gigtools as gt
import datetime


## oil change
#OldDate     = datetime.date( 2024,  6, 19)      # YYYY, MM, DD
#OldMiles    = 175823
#NewDate     = datetime.date( 2024, 12, 28 )      # YYYY, MM, DD
#NewMiles    = 179287
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
gig_files       = [ GigFolder + 'gigs_january_2024.docx'    ,
                    GigFolder + 'gigs_february_2024.docx'   ,
                    GigFolder + 'gigs_march_2024.docx'      ,
                    GigFolder + 'gigs_april_2024.docx'      ,
                    GigFolder + 'gigs_may_2024.docx'        ,
                    GigFolder + 'gigs_june_2024.docx'       ,
                    GigFolder + 'gigs_july_2024.docx'       ,
                    GigFolder + 'gigs_august_2024.docx'     ,
                    GigFolder + 'gigs_september_2024.docx'  ,
                    GigFolder + 'gigs_october_2024.docx'    ,
                    GigFolder + 'gigs_november_2024.docx'   ,
                    GigFolder + 'gigs_december_2024.docx'   ,
                    GigFolder + 'gigs_january_2025.docx'    ]
gigs            = gt.read_gig_files( gig_files, repertwaar, verbose=False)


# Play Count
gt.play_count(gigs, 'rehearsals.txt', repertwaar)


## track song plays in venue.
##   No apostrophes in name
#VenueName   = "Holly Brook East Peoria"
#gt.venue_play_list(VenueName, gigs, repertwaar)


## guitar report
#print()
#gt.guitar_report(gigs, verbose=False)



## mileage report.
#BegDate     = datetime.date( 2024,  1,  1 )      # YYYY, MM, DD
#EndDate     = datetime.date( 2024, 12, 31 )      # YYYY, MM, DD
#gt.mileage_report(gigs, BegDate, EndDate)


## print all gigs with their venue names
#for i,gig in enumerate(second_gigs_copy):
#    print("{0:3d}: {1:<40}: {2:36}".format( i,
#                        gig['title'], gig['venue'] ))


## debug gigs_by_venue(gigs, verbose=False):
#verbose = True
#gigs_copy       = gigs[:]
#venue_gigs  = {}
#while gigs_copy:                             # not empty
#    gig                 = gigs_copy.pop()
#    VName               = gig['venue'].strip().lower()
#    venue_gigs[VName]   = [gig]
#    if verbose:
#        print(f'Got the first {VName}. Searching for more.')
#        if VName == 'the local tap':
#            print('breakpoint here')
#    #   find & remove all matches
#    c           = 0
#    searching   = True
#    while searching:
#        for j in range(len(gigs_copy)):
#            # compare gig['venue'] with VName
#            gig = gigs_copy[j]
#            s   = gt.match_score( VName, gig['venue'].strip().title() )
#            if s >= 60:
#                if verbose:
#                    print(f'\t\tFound another {VName}. Popping...')
#                venue_gigs[VName].append( gigs_copy.pop(j) )
#                break                   # for loop
#        if len(gigs_copy)==0 or len(gigs_copy)<c:
#            searching   = False
#            if verbose:
#                print(f'\tfor loop done with {VName}')
#                print(f'\tNumber of gigs left = {len(gigs_copy)}')
#        c   += 1



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
#SinceDate   = datetime.date( 2024, 5, 13 )      # YYYY, MM, DD
#gigs.sort( key = lambda g: g['date'], reverse=False )
#for gig in gigs:
#    if gig['date'] >= SinceDate:
#        print( "\t{0:<12}: {1:<40}: {2}".format(
#                str(gig['date']), gig['venue'], gig['guitars'] ) )



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

