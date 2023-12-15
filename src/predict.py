from prediction_util import *

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
        # if DNAbert2 returns a 1 for this window, add it to the valid_windows array
        valid_windows.append(window)

# Feed valid_windows to DeepCristl
result = []
enzyme = 'esp'
for window in valid_windows:
    result.append(effciency_predict(dna.replace(os.linesep, ''), enzyme))

print(result)
    