
'''
scratch.py
'''

import gigtools as gt
import datetime


# sort repertwaar on most recent playdate, and display
played_songs    = []
# get the earliest date
MinDate         = datetime.date.today()
for song in repertwaar:
    if song['playcount'] > 0:
        played_songs.append(song)
        MinDate = min( MinDate, min(song['playdates']) )
# write earliest date to unplayed songs
for song in repertwaar:
    if song['playcount'] == 0:
        song['playdates'].append(MinDate)
# sort the repertwaar
repertwaar.sort( key = lambda s: max(s['playdates']) )
# analysis and printout
print('play counts by song:')
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
    print( '\t{0:<40}: {1:3d} plays : {2}'.format(
                song['title'].removesuffix('*'),
                song['playcount'], DeltaString ) )



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

