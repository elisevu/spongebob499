# import bleu
# import rouge
import numpy as np
import os
import re
import nltk

path = 'archive/SpongeBob_SquarePants_Transcripts'
# print(os.path.exists(path))
# with open('all_spongebob.txt', 'w', encoding='utf8') as sponge:
#     for filename in os.listdir('archive/SpongeBob_SquarePants_Transcripts'):
#         current = path + '/' + filename
#         with open(current, 'r', encoding='utf8') as file:
#             now = file.read()
#             sponge.write(filename + '\n')
#             sponge.write(now)
            # sponge.write('\n')
    
#read in all spongebob scripts, separate characters from dialogue/actions
with open('all_spongebob.txt', 'r', encoding='utf8') as sponge:
    sponge_script = sponge.read()
    sponge_script = sponge_script.split('\n')

separated = []
for line in sponge_script:
    separated.append(line.split(': '))
#tags characters, titles, dialogue and context parts
tag = {}
for line in separated:
    for part in line:
        if part == '':
            break
        if part.find('.txt') != -1:
            tag[part] = 'EPISODE'
            break
        try:
            context = re.findall(r"\[+.+\]", part)
        except AttributeError:
            context = ''
        if part == line[0] and context == '':
            tag[part] = 'CHAR'
        else:
            tag[tuple(context)] = 'CONTEXT'
            dialogue = ''
            for each in context:
                dialogue = dialogue + (part.replace(each, ''))
                dialogue.strip()
            tag[dialogue] = 'DIALOGUE'

        


def process_and_get_words():
    # setting up futurama dataset
    with open('archive/Futurama/only_spoken_text.csv', 'r', encoding='utf8') as f_spoken_text:
        f_lines_w_speaker = f_spoken_text.readlines()
    
    # grabbing the third column of the csv, and not slicing any commas within it
    f_dialogue = []
    for line in f_lines_w_speaker:
        formatted = line.split(',',3)
        current_dialog = formatted[2] + ": " + formatted[3]
        f_dialogue.append(current_dialog)
    
    
    # setting up spongebob dataset
    with open('all_spongebob.txt', 'r', encoding='utf8') as s_spoken_text:
        s_lines_w_speaker = s_spoken_text.readlines()
    
    # stripping out empty space and episode titles
    s_dialogue = []
    for line in s_lines_w_speaker:
        if line.__contains__(".txt"):
            continue
        elif line == '' or line == ' ':
            continue
        else:
            s_dialogue.append(line)
    
    with open('actual_both_dialogues.txt', 'w', encoding='utf8') as both:
        valid = lambda l : l != '\n' and l != ' ' and l != '' and l[0] != ' ' and l[0] != '['
        for line in f_dialogue:
            if valid(line):
                both.write(line.replace('"', '').replace('<poem>', '').replace(':  ', ': ', 1))

        
        for line in s_dialogue:
            if valid(line):
                both.write(line)
        

    
    
    
    
    # start = time.time()
    words = []
    for sent in f_dialogue:
        words+=(nltk.word_tokenize(sent))
        
    for sent in s_dialogue:
        words+=(nltk.word_tokenize(sent))
        
    return words



# words = process_and_get_words()

def make_sent(length=13):
    sent = ""
    for i in range(length):
        sent += words[np.random.randint(0, len(words))] + " "
    return sent

print(make_sent())



