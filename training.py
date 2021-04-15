import nltk

with open('actual_both_dialogues.txt', 'r', encoding='utf8') as doc:
    text_tokenized = []
    for line in doc.readlines():
        try:
            speaker, dialogue = line.split(': ', 1)
            dialogue = nltk.word_tokenize(dialogue.lower())
            text_tokenized.append(speaker.lower()+":") 
            text_tokenized += dialogue
        except ValueError:
            print(line)


word_to_ix = {key:val for val,key in enumerate(set(text_tokenized))}
ix_to_word = {val:key for key,val in word_to_ix.items()}

int_script = [word_to_ix[word] for word in text_tokenized]


from torch.utils.data import TensorDataset, DataLoader

def batch_data(int_script, seq_length, batch_size):
    f, t = [], []

    # separating the speaker from the line
    for i in range(len(int_script) - seq_length):
        f.append(int_script[i : i+seq_length])
        t.append(int_script[i+seq_length])

    data_set = TensorDataset(torch.tensor(f, dtype=torch.long), torch.tensor(t, dtype=torch.long))
    
    return DataLoader(data_set, shuffle=True, batch_size=batch_size)

