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



#'archive/SpongeBob_SquarePants_Transcripts'