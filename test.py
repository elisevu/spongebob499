import bleu
import rouge
import numpy as np
import os

path = 'archive/SpongeBob_SquarePants_Transcripts'
# print(os.path.exists(path))
with open('all_spongebob.txt', 'w', encoding='utf8') as sponge:
    for filename in os.listdir('archive/SpongeBob_SquarePants_Transcripts'):
        current = path + '/' + filename
        with open(current, 'r', encoding='utf8') as file:
            now = file.read()
            sponge.write(filename + '\n')
            sponge.write(now)
            sponge.write('\n')
    
#read in all spongebob scripts, separate characters from dialogue/actions
with open('all_spongebob.txt', 'r', encoding='utf8') as sponge:
    sponge_script = sponge.read()
    sponge_script = sponge_script.split('\n')

separated = []
for line in sponge_script:
    separated.append(line.split(': '))
# print(separated[0:5])
    



#'archive/SpongeBob_SquarePants_Transcripts'