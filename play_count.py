
# play_count.py
''' Reads gig data from .docx files and rehearsals.txt to display
    the number of times each song in the repertwaar has been played'''

import gigtools as gt
import datetime


## read in the repertwaar--a list of song dictionaries
#repertwaar      = gt.read_repertwaar()
#
## read a set of DOCX files containing multiple gigs using docx,
## and print play counts.
#GigFolder       = 'S:\\will\\documents\\OneDrive\\2024\\gigtools\\gigfiles\\'
#GigFile         = 'multi.docx'
#gig_files       = [ GigFolder + 'gigs_january_2024.docx'    ,
#                    GigFolder + 'gigs_february_2024.docx'   ,
#                    GigFolder + 'gigs_march_2024.docx'      ,
#                    GigFolder + 'gigs_april_2024.docx'      ,
#                    GigFolder + 'gigs_may_2024.docx'        ,
#                    GigFolder + 'gigs_june_2024.docx'       ,
#                    GigFolder + 'gigs_july_2024.docx'       ]
#gigs            = gt.read_gig_files(gig_files, repertwaar)


# read rehearsals.txt
with open('rehearsals.txt', 'r') as file:
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
            score   = gt.score_line(repertwaar, line.strip())
            if score >= 70.0:
                # increment the match count
                matches += 1
        if matches > BestMatches:
            # song list might be found
            BestBlock   = block
            BestMatches = matches
            break
    reh_songs   = gt.match_gig_songs(repertwaar, BestBlock)
    print(f'\t{len(reh_songs)} songs found' )
    print(f'\t{len(reh_lines)} text lines' )
    for song in reh_songs:
        song['playcount']  += 1
        song['playdates'].append(rehearse_dates[i])
    rehearsal   = { 'Date'  : rehearse_dates[i]     ,
                    'Songs' : reh_songs             ,
                    'Lines' : reh_lines             }
    rehearsals.append(rehearsal)

# Freshness
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


# analysis and printout
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


