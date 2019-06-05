# Moves between lists and dictionary. Loops over list.
words = ['color', 'color', 'colour', 'amok', 'amok', 'amuck', 'advisor', 'adviser', 'pepper']
canonical_spellings = ['color', 'amuck', 'adviser', 'pepper']
mappings = {'colour': 'color', 'amok': 'amuck', 'advisor': 'adviser'}

#make an empty list
new_list = []

#loop over list of words
for word in words:
    if word in words:
        if word in mappings:
            #if a word is mispelled do something
            #correct the spelling using the mapping dictionary
            corrected_word = mappings[word]
            # add corrected_word
            new_list.append(corrected_word)

        else:
            new_list.append(word)
print(new_list)
