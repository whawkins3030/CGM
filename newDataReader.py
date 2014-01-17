
# File: newDataReader.py

# Coded by: Will Hawkins

# Date: Dec 19, 2013


# Initializes the "diatonic_data" 7x7 transition matrix.
# The array acts as the first-order Markov Chain for chord changes. 
# Its use is summarized like so: "Chord x is followed by chord y 
# with probability z [value 0-100]."

diatonic_data = []
diatonic_data.append(None)
for i in range(1,8):
    r = []
    r.append(None)
    for j in range(1,8):
        r.append(0)
    diatonic_data.append(r)


# This array will act similarly to the "diatonic_data" array
# except that it records the first chord of every song. 
# (The starting chord of a song section is significant 
# because it determines the mode.)
first_chord_d = [None, 0,0,0,0,0,0,0]



# Processes all data from a chord progression file and returns the 
# completed "diatonic_data" and "first_chord_d" arrays. 
def getChordArrays(filename):
    infile = open(filename, 'r')
    for i in range(3):
        line = infile.readline()

    all_chord_total = 0
    while line != "":
        seq = line.split()
        ind = 0
        seq_length = len(seq)

        for c in seq:
            current_chord_x = c[0]
            # First chord
            if ind == 0:
                first_chord_d[eval(current_chord_x)] += 1
            # Other chords
            if ind != (seq_length-1):
                next_chord_y = seq[ind+1][0]
            # Final chord (wraps around to first chord)
            else:
                next_chord_y = seq[0][0]
            diatonic_data[eval(current_chord_x)][eval(next_chord_y)] += 1
            ind += 1
            all_chord_total += 1

        for i in range(4):
            line = infile.readline()

    infile.close()

    # Counts the total number of chords 1-7 each, and then 
    # converts diatonic_data into %'s
    chordCounts = [None,0,0,0,0,0,0,0]
    for i in range(1,8):
        for n in diatonic_data[i][1:8]:
            chordCounts[i] += n
        for j in range(1,8):
            count = chordCounts[i]
            if count != 0:
                diatonic_data[i][j] *= 100/count
                diatonic_data[i][j] = diatonic_data[i][j]

    # Counts total number of first chords and then converts to %'s
    first_chord_total = 0
    for n in first_chord_d[1:]:
        first_chord_total += n
    for i in range(1,8):
        first_chord_d[i] *= 100/first_chord_total
        first_chord_d[i] = first_chord_d[i]

    return diatonic_data, first_chord_d, all_chord_total, first_chord_total



# Prints all chord-prog database statistics from inputted file.
def printDataStats(filename):
    d_d, f_d, all_chord_total, first_chord_total = getChordArrays(filename)

    print("Total # of songs processed:", first_chord_total)
    print()
    print("Total # of chords processed:", all_chord_total)
    print()

    f_perc_msg = "First-chord percentages:"
    for i in range(1,8):
        f_perc_msg += str(f_d[i]) + "% "
    print(f_perc_msg)
    print()

    roman_num_notation = ["", "  I", " ii", "iii", " IV", "  V", " iv", "iiv"]
    print("Main chord-change percents:   ____I___ii__iii___IV____V___iv___iiv")
    for i in range(1,8):
        interval = roman_num_notation[i]
        m = "                          " + interval + ":"
        for j in range(1,8):
            d = str(d_d[i][j])
            space = (8-len(d))*" "
            m+= space + d
            #if len(d) == 1:
                #m += "    " + d      ##NOTE: I made changes to this on 12/9/13 so I could see the non-rounded matrix vals..fix formatting
            #elif len(d) == 2:
                #m += "   " + d
            #elif len(d) == 3:
                #m += "  " + d
        print(m)


printDataStats("CGM_chords_all.txt")


