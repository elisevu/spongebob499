import nltk
import argparse
import torch
import numpy as np
from torch import nn, optim
from torch.utils.data import TensorDataset, DataLoader
from model import Model
from dataset import Dataset

def train(dataset, model, args):
    model.train()

    dataloader = DataLoader(dataset, batch_size=args.batch_size)
    criterion = nn.CrossEntropyLoss()
    optimizer = optim.Adam(model.parameters(), lr=0.001)

    for epoch in range(args.max_epochs):
        state_h, state_c = model.init_state(args.sequence_length)

        for batch, (x, y) in enumerate(dataloader):
            optimizer.zero_grad()

            y_pred, (state_h, state_c) = model(x, (state_h, state_c))
            loss = criterion(y_pred.transpose(1, 2), y)

            state_h = state_h.detach()
            state_c = state_c.detach()

            loss.backward()
            optimizer.step()

            print({ 'epoch': epoch, 'batch': batch, 'loss': loss.item() })

def predict(dataset, model, text, next_words=100):
    model.eval()

    words = text.split(' ')
    state_h, state_c = model.init_state(len(words))

    for i in range(0, next_words):
        x = torch.tensor([[dataset.word_to_index[w] for w in words[i:]]])
        y_pred, (state_h, state_c) = model(x, (state_h, state_c))

        last_word_logits = y_pred[0][-1]
        p = torch.nn.functional.softmax(last_word_logits, dim=0).detach().numpy()
        word_index = np.random.choice(len(last_word_logits), p=p)
        words.append(dataset.index_to_word[word_index])

    return words

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


def batch_data(int_script, seq_length, batch_size):
    f, t = [], []

    # separating the speaker from the line
    for i in range(len(int_script) - seq_length):
        f.append(int_script[i : i+seq_length])
        t.append(int_script[i+seq_length])

    data_set = TensorDataset(torch.tensor(f, dtype=torch.long), torch.tensor(t, dtype=torch.long))
    
    return DataLoader(data_set, shuffle=True, batch_size=batch_size)

parser = argparse.ArgumentParser()
parser.add_argument('--max-epochs', type=int, default=10)
parser.add_argument('--batch-size', type=int, default=256)
parser.add_argument('--sequence-length', type=int, default=4)
args = parser.parse_args()

dataset = Dataset(args)
model = Model(dataset)

train(dataset, model, args)
print(predict(dataset, model, text='Spongebob Squarepants'))