import os, math

def get_distance(word_fr1, word_fr2):
    #--- paper is already merged ---#
    if (word_fr1 is None or word_fr2 is None):
        return -float('inf')
    
    ans = 0
    for i in range(no_of_words):
        ans += word_fr1[i]*word_fr2[i]
    return ans
    
fin = open("data", 'r')
temp_data = fin.readlines()
#print "\ntemp data :", temp_data, "has", len(temp_data), "lines"

#--- Number of Papers ---#
no_of_papers = len(temp_data)//3
print "\nno of papers :", no_of_papers

no_of_words = len(temp_data[-2].split())
print "\nno of words :", no_of_words

titles = []
authors = []
word_frs = []

#--- Separating Title, Author, Word-Frequency ---#
print "\noriginal word_frs :"
for i in range(no_of_papers):
    
    title_curr, author_curr = temp_data[i*3].split('&')
    title_curr = title_curr.split(':')[1].strip()
    author_curr = author_curr.split(':')[1].strip()

    word_fr_curr = map(int, temp_data[i*3 + 1].split())
    word_fr_curr = word_fr_curr + [0]*(no_of_words - len(word_fr_curr))

    print title_curr, 'by', author_curr
    print '>>>', word_fr_curr
    print ''
    
    titles.append(title_curr)
    authors.append(author_curr)
    word_frs.append(word_fr_curr)

#--- Finding Max Fr ---#
max_fr = 0
for i in range(no_of_papers):
    max_fr = max(max_fr, max(word_frs[i]))

#--- Calculating Equalizer ---#
eq = 0#max_fr/2

print "\nmax fr :", max_fr
print "eq :", eq

#--- Finding max_fr for each word ---#
max_fr = [0]*no_of_words
for i in range(no_of_papers):
    for j in range(no_of_words):
        max_fr[j] = max(max_fr[j], word_frs[i][j])

#--- Modifying words_frs ---#
for i in range(no_of_papers):
    for j in range(no_of_words):
        word_frs[i][j] /= float(max_fr[j])

parent = {}
for i in range(no_of_papers):
    parent[i] = i

def find(x):
    while (parent[x] != x):
        x = parent[x]
    return x

def union(i, j):
    pi = find(i)
    pj = find(j)
    parent[pj] = pi

#--- Forming cluster ---#
no_of_papers_temp = no_of_papers
while (True):
    matrix = []
    for i in range(no_of_papers_temp):
        matrix.append(['_']*no_of_papers_temp)

    #--- Finding closest pair ---#        
    curr_closest_pair = None
    curr_closest_dist = -float('inf')

    for i in range(no_of_papers_temp):
        for j in range(i+1, no_of_papers_temp):
            matrix[i][j] = get_distance(word_frs[i], word_frs[j])
            if (matrix[i][j] > curr_closest_dist):
                curr_closest_dist = matrix[i][j]
                curr_closest_pair = (i, j)
                
    print "\n*************************************"    

    print "\nmodified word_frs :"
    for i in range(no_of_papers):
        print titles[i], 'by', authors[i]
        print '>>>', word_frs[i]

    print "\nclosest pair :", curr_closest_pair    
    print "\ndistances :"
    for i in range(no_of_papers_temp):
        for j in range(no_of_papers_temp):
            print matrix[i][j], '\t', 
        print ''

    #--- Terminating condition ---#
    if (curr_closest_dist <= 0.2):
        print "\nno two paper are close enough to cluster"
        break

    #--- Merge current closest pair ---#
    p1 = curr_closest_pair[0]
    p2 = curr_closest_pair[1]
    union(p1, p2)

    #no_of_papers_temp -= 1 #--- commented so that matrix remains okay ---#

    #print word_frs, '->', 
    for i in range(no_of_words):
        word_frs[p1][i] = int(math.ceil((word_frs[p1][i] + word_frs[p2][i])/2.0))
    word_frs[p2] = None
    #print word_frs

print "\n*************************************\n"

count = 1
for i in range(no_of_papers):
    if (i == find(i)):
        print "cluster", count
        for j in range(i, no_of_papers):
            if (find(j) == i):
                print titles[j], 'by', authors[j]
        count += 1
        print ''
    

    
    
     
