#import des bibliothèques
import sys
import re

def separate(): 
    
    sequence=[]
    variable=[]
    seq=True
    var=False
    code='[A-C-G-T]'


    #lecture du FASTA avec stdin
    for line in sys.stdin:
        line=line.rstrip()
        if line.startswith(";"):
            pass
        elif line.startswith(">"):
            pass
        elif re.match(code,line)!=None and seq==True :
            sequence.append(line)
            seq=False
            var=True
        elif re.match(code,line)!=None and var==True :
            variable.append(line)
            seq=True
            var=False
    print(sequence)
    print(variable)


separate()
    
        
        






    


