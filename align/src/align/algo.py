#import des bibliothèques
import sys
import re
import argparse
import logging

logger=logging.getLogger(__name__)

def compare(a,b,Indel,Mismatch,Match):
        add=None
        if a==b:
            add=Match
        elif a=='-' or b=='-':
            add=Indel
        else:
            add=Mismatch
        return add
        
    
def fill_table(seq1,seq2,indel,match,mismatch):
    cols=len(seq1)+1
    rows=len(seq2)+1

    M= [[0 for _ in range(cols)] for _ in range (rows)]

    for i in range (1,rows):
        M[i][0]=mismatch*i
    for j in range(1,cols):
        M[0][j]=mismatch*j

    for i in range (1,rows):
        for j in range (1,cols):
            add=compare(seq2[i-1],seq1[j-1],indel,mismatch,match)
            case1=M[i-1][j-1]+add
            case2=M[i][j-1]+add
            case3=M[i-1][j]+add
            M[i][j]=min(case1,case2,case3)
    
    print (M)


def traceback(seq1, seq2, M, indel, match, mismatch):
    align1, align2 = "", ""
    i, j = len(seq2), len(seq1)

    while i > 0 or j > 0:
        current_score = M[i][j]
        diagonal = M[i - 1][j - 1] if i > 0 and j > 0 else float('inf')
        left = M[i][j - 1] if j > 0 else float('inf')
        up = M[i - 1][j] if i > 0 else float('inf')

        if current_score == diagonal + compare(seq2[i - 1], seq1[j - 1], indel, mismatch, match):
            align1 = seq1[j - 1] + align1
            align2 = seq2[i - 1] + align2
            i -= 1
            j -= 1
        elif current_score == left + compare('-', seq1[j - 1], indel, mismatch, match):
            align1 = seq1[j - 1] + align1
            align2 = '-' + align2
            j -= 1
        else:
            align1 = '-' + align1
            align2 = seq2[i - 1] + align2
            i -= 1

    return align1, align2

if __name__ == "__main__":
    sequence = []
    variable = []
    seq = False
    var = False
    code = '[A-C-G-T]+'
    
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

    M = fill_table(sequence[0], variable[0], -2, 1, -1)
    
    for row in M:
        print(row)

    alignment1, alignment2 = traceback(sequence[0], variable[0], M, -2, 1, -1)

    print("Alignment 1:", alignment1)
    print("Alignment 2:", alignment2)


