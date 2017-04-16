import os
can_stem = True

if (can_stem):
    from nltk.stem.snowball import SnowballStemmer

def sort_utility(x):
    return x[1]

def get_keywords_from_abstract(string, n):
    #--- Returns 'n' most-frequent keywords and their frequencies from the 'string' ---#
    if (string is None):
        return [], []

    abstract_word_list = string.split()
    
    temp_wf = {}
    for word in abstract_word_list:
        word = word.lower()
        if (can_stem):
            word = str(stemmer.stem(word))
        if (word not in stop_words):
            temp_wf[word] = temp_wf.get(word, 0) + 1

    sorted_wf = sorted(temp_wf.items(), reverse = True, key = sort_utility)

    word_list = []
    freq_list = []
    for i in range(n):
        word_list.append(sorted_wf[i][0])
        freq_list.append(sorted_wf[i][1])

    return word_list, freq_list

def get_keywords_listed(string):
    #--- Returns all the keywords listed in the 'string' and setting frequency = 20---#
    keywords = string.split(',')
    for i in range(len(keywords)):
        keywords[i] = keywords[i].strip().lower()
        if (can_stem):
            keywords[i] = str(stemmer.stem(keywords[i]))
    return keywords

#--- Cleaning old data ---#
fin = open("data", "w")
fin.close()

fin = open("words", "w")
fin.close()

#--- Creating Stemmer ---#
if (can_stem):
    stemmer = SnowballStemmer('english')

#--- Getting the list of stop-words ---#
fsw = open("stopwords", 'r')
stop_words = fsw.readlines()
for i in range(len(stop_words)):
    #--- Cleaning stop-words ---#
    stop_words[i] = stop_words[i].strip()
    if (can_stem):
        stop_words[i] = str(stemmer.stem(stop_words[i]))
fsw.close()

#--- Change directory to Papers ---#
os.chdir(os.getcwd() + '/Papers')

#--- Read all files and add to data ---#
file_names = os.listdir(os.getcwd())

no_of_words_to_extract_from_abstract = 5

for file_name in file_names:
    title = None
    author = None 
    abstract = None
    keywords = None
    if (file_name.endswith('.txt')):
        fin = open(file_name, 'r')
        for line in fin:
            #--- Trim blank lines ---#
            if (len(line) > 1):
                if (line.startswith('Title')):
                    title = line.split(':')[1].strip()
                elif (line.startswith('Author')):
                    author = line.split(':')[1].strip()
                elif (line.startswith('Abstract')):
                    abstract = line.split(':')[1].strip()
                elif (line.startswith('Keywords')):
                    keywords = line.split(':')[1].strip()
        fin.close()
        
        #--- Get additional keywords ---#
        keywords_from_abstract, frequencies_from_abstract = get_keywords_from_abstract(abstract, no_of_words_to_extract_from_abstract)
        keywords_listed = get_keywords_listed(keywords)
 
        #--- Changing directory going outside 'Papers' directory ---#
        os.chdir(os.getcwd()[:-7]) 

        #--- Read all words from 'words' file ---#
        fin_words = open('words', 'r')
        words = fin_words.readlines()
        fin_words.close()

        #--- Combining keywords (from abstract and those listed) and frequencies ---#   
        keywords_combined = []
        frequencies_combined = []
        weight_of_keywords = 10
        for word in keywords_from_abstract + keywords_listed:
            #--- Skipping repeated words ---#
            if (word in keywords_combined):
                continue
            if (word in keywords_from_abstract and word in keywords_listed):
                keywords_combined.append(word)
                frequencies_combined.append(weight_of_keywords + frequencies_from_abstract[keywords_from_abstract.index(word)])
            elif (word in keywords_from_abstract):
                keywords_combined.append(word)
                frequencies_combined.append(frequencies_from_abstract[keywords_from_abstract.index(word)])
            else:
                keywords_combined.append(word)
                frequencies_combined.append(weight_of_keywords)

        
        #--- Printing temp data ---#
        print title, author, ':', keywords_combined, '->', frequencies_combined

        
        #--- Calculating frequencies of existing words --- #
        visited  = [False]*len(keywords_combined) #--- To track the new words >> all the words not visited at the end are new words ---#

        frequency_for_curr_file = []
        for word in words:
            word = word.strip() #--- removing '\n' from the end ---#
            if word in keywords_combined:
                pos = keywords_combined.index(word)
                visited[pos] = True
                frequency_for_curr_file.append(frequencies_combined[pos])
            else:
                frequency_for_curr_file.append(0)

        #--- Adding new words and their frequencies ---#
        fout_words = open('words', 'a') #--- To add new words ---#
        for i in range(len(keywords_listed)):
            if (not visited[i]):
                fout_words.write(keywords_combined[i].strip()+'\n')
                frequency_for_curr_file.append(frequencies_combined[i])
        fout_words.close()

        #--- Adding data to the 'data' file ---#
        fout_data = open('data', 'a')
        fout_data.write('title : ' + title + ' &  author : ' + author + '\n')
        temp = map(str, frequency_for_curr_file)
        fout_data.write(' '.join(temp) + '\n')
        fout_data.write('\n')
        fout_data.close()    
 
        #--- Changing directory going inside 'Papers' directory ---#
        os.chdir(os.getcwd() + '/Papers')
    else:
        print 'ERROR :', file_name, 'is in wrong format'
    
    print '----------'*5
    
