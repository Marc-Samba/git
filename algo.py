#import des bibliothèques
import sys
import re
import argparse

    
sequence=[]
variable=[]
seq=False
var=False
code='[A-C-G-T]+'


#lecture du FASTA avec stdin
for line in sys.stdin:
    if re.match(code,line)==None:
        if seq==True and var==True:
            seq,var=False,False
    else:
        n=len(line)
        if var==False:
            if seq==False:
                sequence.append(line.rstrip())
                seq=True
            else :
                variable.append(line.rstrip())
                var=True
        else : 
            variable[-1]=variable[-1]+line.rstrip()
print(sequence)
print(variable)


def fill_table(seq1,seq2):
    cols=len(seq1)+1
    rows=len(seq2)+1

    M= [[0 for _ in range(cols)], for _ in range (rows)]

    for i in range (1,line):
        pass
    for j in range(1,cols):
        pass