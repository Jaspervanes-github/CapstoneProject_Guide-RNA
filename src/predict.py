import torch
from transformers import AutoTokenizer, AutoModel

tokenizer = AutoTokenizer.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)
model = AutoModel.from_pretrained("zhihan1996/DNABERT-2-117M", trust_remote_code=True)

dna = "ACGTAGCATCGGATCTATCTATCGACACTTGGTTATCGATCTACGAGCATCTCGTTAGC"
dna_list = list(dna)

window_size = 3

def sliding_window(elements, window_size):
    
    if len(elements) <= window_size:
       return elements    
    for i in range(len(elements)- window_size + 1):
        print(elements[i:i+window_size])
        
window_list = sliding_window(dna_list, window_size)
valid_windows = []
for window in window_list:
    # Feed the window to DNAbert2
    if(True):
        valid_windows.append(window)

# Feed valid_windows to DeepCristl

    