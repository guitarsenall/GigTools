
'''
scratch.py
'''

import gigtools as gt

# detect a partial match and return score
def match_score(title, line):
    ''' new version that takes length mismatch into account '''
    title   = title.strip()
    line    = line.strip()
    match   = -abs( len(title) - len(line) )
    for i in range( min(len(title),len(line)) - 1 ):
        if line[i:i+2] in title:
            match += 1
    return match / (len(title)-1) * 100

#title   = 'Here, There and Everywhere'
#line    = 'Guitars: 814ce, V700, 812ce'
#match_score( title, line )

def score_line(repertwaar, line):
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


# read a DOCX gig file using docx
import docx
import os
import unicodedata
ScoreThreshold  = 70.0
repertwaar      = gt.read_repertwaar()
GigFolder       = 'S:\\will\\documents\\OneDrive\\2024\\gigtools\\gigfiles\\'
GigFile         = 'Tres Rojas 91023.docx'
doc = docx.Document(GigFolder + GigFile)
allText = []
for docpara in doc.paragraphs:
    allText.append(unicodedata.normalize('NFKD',docpara.text))
blocks  = []
this_block  = []
for line in allText:
    if line == ' ':
        blocks.append(this_block[:])    # copy the list
        this_block  = []
    else:
        this_block.append(line)
for block in blocks:
    if len(block) >= 5:
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
gig_songs   = gt.match_gig_songs(repertwaar, song_list)
for song in gig_songs:
    song['playcount']  += 1
for song in repertwaar:
    print(song['title'].removesuffix('*'), ': ',
            str(song['playcount']), ' plays' )


## read a PDF gig file using pypdf
#from pypdf import PdfReader
#import os
#os.chdir('S:\\will\\documents\\OneDrive\\2024\\gigtools')
#reader = PdfReader('gigfiles/Tres Rojas 91023.pdf')
#print(len(reader.pages))
#page = reader.pages[0]
#text = page.extract_text()
#print(text)


## detect a partial match and return score
#def match_score(title, line):
#    match   = 0
#    for i in range( min(len(title),len(line)) - 1 ):
#        if line[i:i+2] in title:
#            match += 1
#    return match / (len(title)-1) * 100


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

