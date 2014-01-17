
# File: newSongGen.py

# Coded by: Will Hawkins

# Date: Dec 19, 2013


from newDataReader import *
from random import *

# Gets chord data file name, generates array stats. 
filename = "CGM_chords_all.txt"
printDataStats(filename)
diat_data, first_data, diat_total, first_total = getChordArrays(filename)

print()
print()
print("TEST ZONE")
print(diat_data)
print()
print(first_data)
print(diat_total)
print(first_total)
print()

# Initializes song data structure.
verse = {"Chords":[], "Melody":[]}
chorus = {"Chords":[], "Melody":[]}
bridge = {"Chords":[], "Melody":[]}
song = [verse, chorus, bridge]

# Generates the first chords of all three song sections. Note: First chords of
# Chorus and Bridge must be different.
sectIndex = 0
for sect in song:
    while len(sect["Chords"]) < 1:
        rand_perc = randrange(1,100)
        summ = 0
        chordInt = 1
        while summ < rand_perc:
            print()
            print("chordInt:" + str(chordInt))
            print("current chords = " + str(sect["Chords"]))
            print(first_data)
            print("SUM " + str(summ))
            print("rand_perc " + str(rand_perc))
            summ += first_data[chordInt]
            chordInt += 1
        chordInt -= 1

        # Makes sure the chorus and the bridge
        # start on different chords.
        checksAllGood = True
        if sectIndex == 2 and chordInt == chorus_cho:
            checksAllGood = False

        if checksAllGood:
            if sectIndex == 1:
                chorus_cho = chordInt
            sect["Chords"].append(chordInt)
            sectIndex += 1


# Finishes all section chord progressions.
# Prevents: 2nd/3rd chord duplicates,
# 1st/5th chord duplicates. Only one
# 8 bar section per song
sectIndex = 0
for sect in song:
    chordIndex = 0
    chordBranch = diat_data[sect["Chords"][0]]

    if sectIndex == 0:
        lenSection = 4 * choice([1,1,2])
        verseLength = lenSection
    elif sectIndex == 1:
        lenSection = 4
    elif sectIndex == 2:
        if verseLength == 8:
            lenSection = 4
        else:
            lenSection = 4 * choice([1,2])

    while len(sect["Chords"]) < lenSection:
        rand_perc = randrange(100)
        summ = 0
        chordInt = 1
        while summ < rand_perc:
            summ += chordBranch[chordInt]
            chordInt += 1
        chordInt -= 1

        checksAllGood = True

        # Prevents 2nd&3rd-chord duplicates
        if chordIndex % 4 == 2:
            if sect["Chords"][chordIndex-1] == chordInt:
                checksAllGood = False

        # Prevents 1st&5th-chord duplicates
        if chordIndex == 3:
            if sect["Chords"][0] == chordInt:
                checksAllGood = False
                
        if checksAllGood:
            sect["Chords"].append(chordInt)
            chordBranch = diat_data[chordInt]
            chordIndex += 1
    sectIndex += 1


# Returns a list of chord-tones for an inputted diatonic number.
def getPossChordTones(chordRootNum, diatonic_range):
    chordTones = []
    for i in [0, 2, 4, 7, 9, 11, 14]:
        tone = chordRootNum + i
        if tone <= diatonic_range:
            chordTones.append(tone)
        else:
            break
    return chordTones

octave_range = 2
diatonic_note_range = octave_range * 7 + 1
max_skeleton_jump = 3

for sect in song:
    sect["transMelody"] = []
    sect["transHarmony"] = []
    for i in range(len(sect["Chords"])):
        sect["Melody"].append([0,0,0,0,0,0,0,0])
        sect["Harmony"].append([0,0,0,0,0,0,0,0])
        sect["transMelody"].append([0,0,0,0,0,0,0,0])
        sect["transHarmony"].append([0,0,0,0,0,0,0,0])


# Probability of note x being selected (settled on even probability). 
melody_matrix = [None, 100*1/7, 100*1/7, 100*1/7, 100*1/7, 100*1/7, 100*1/7, 100*1/7]

for track in ["Melody"]:
    for sect in song:
        prevChordInd = 1

        noteDist = 3

        chordInd = 0
        for chord in sect["Chords"]:
            for note in [0,4]:
                possChordTones = getPossChordTones(chord, diatonic_note_range)
                cont = True
                while cont:
                    jumpVal = randrange(max_skeleton_jump) * choice([-1,1])
                    newInd = jumpVal + prevChordInd
                    if newInd < len(possChordTones) and newInd > 0:
                        if note == 2:
                            if sect[track][chordInd][note-2] != possChordTones[newInd]:
                                cont = False
                        else:
                            cont = False
                sect[track][chordInd][note] = possChordTones[newInd]
            
            for note in [1,2,3,5,6,7]:
                not_finished = True
                while not_finished:
                    summ = 0
                    rand_perc = randrange(100)
                    for interv in range(1,8):
                        lastNote = sect[track][chordInd][note-1]
                        if (rand_perc < melody_matrix[interv]+summ) and (interv != lastNote) and (abs((interv%7)-(lastNote%7))<noteDist):
                            sect[track][chordInd][note] = interv
                            not_finished = False
                            break
                        else:
                            summ += melody_matrix[interv]
            chordInd += 1

# Eliminates notes depending on position in half-bar. 
for sect in song:
    for line in [sect["Melody"]]:
        for bar in line:
            r1 = randrange(10)
            if r1 == 0 or r1 == 1:
                bar[0] = "-"

            r2 = randrange(3)
            if r2 == 0 or r2 == 1:
                bar[1] = "-"

            r3 = randrange(6)
            if r3 == 0 or r3 == 1:
                bar[2] = "-"

            r4 = randrange(3)
            if r4 == 0 or r4 == 1:
                bar[3] = "-"

            r5 = randrange(8)
            if r5 == 0 or r5 == 1:
                bar[4] = "-"

            r6 = randrange(3)
            if r6 == 0 or r6 == 1:
                bar[5] = "-"

            r7 = randrange(6)
            if r7 == 0 or r7 == 1:
                bar[6] = "-"

            r8 = randrange(3)
            if r8 == 0 or r8 == 1:
                bar[7] = "-"


def convertToLetter(num):
    if num == "-": return "-"
    letterVals = ["B", "C", "D", "E", "F", "G", "A"]
    ind = num % 7
    return letterVals[ind]


keys = ["C", "G", "Eb", "F", "D"]


for sect in song:
    for bar in sect["Melody"]:
        indy = 0
        for note in bar:
            sect["transMelody"][sect["Melody"].index(bar)][indy] = convertToLetter(note)
            indy += 1
    for bar in sect["Harmony"]:
        indy = 0
        for note in bar:
            sect["transHarmony"][sect["Harmony"].index(bar)][indy] = convertToLetter(note)
            indy += 1


notes = []


from pyknonfinalNEW.genmidi import Midi
from pyknonfinalNEW.music import *

        
print()       
print("Composition #" + str(randrange(10000)) + ":")
print("Key:", choice(keys), "major")
print()
print("Verse:", song[0]["Chords"])
for halfbar in song[0]["transMelody"]:
    for note in halfbar:
        if note == "-":
            notes.append(Rest(dur=1/8))
        else:
            thing = note + "5"
            notes.append(Note(thing,dur=1/8))
        
    print(halfbar)
print()
print("Chorus:", song[1]["Chords"])
for halfbar in song[1]["transMelody"]:
    print(halfbar)
print()
print("Bridge:", song[2]["Chords"])
for halfbar in song[2]["transMelody"]:
    print(halfbar)


notes1 = NoteSeq(notes)
print(notes1)
midi = Midi(1, tempo=90)
midi.seq_notes(notes1, track=0)
midi.write("cgmtest.mid")


