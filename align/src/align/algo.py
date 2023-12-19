#import des bibliothèques
import sys
import re
import argparse
import logging

logger=logging.getLogger(__name__)

if __name__=="__main__":

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


    def compare(a,b,Indel,Mismatch,Match):
        add=None
        if a==b:
            add=Match
        elif a=='-' or b=='-':
            add=Indel
        else:
            add=Mismatch
        
    
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
                add=compare(seq2[i],seq1[j])
                case1=seq2[i-1]+add
                case2=seq2[i]+add
                case3=seq1[j]+add
                M[i][j]=min(case1,case2,case3)
            



