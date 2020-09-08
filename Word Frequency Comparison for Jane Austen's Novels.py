import requests
from bs4 import BeautifulSoup
import nltk
import matplotlib as plt
import pandas as pd
from nltk.corpus import stopwords
from tika import parser 

# URLs for Jane Austen's "Pride and Prejudice" and "Emma"
PandP = 'https://www.gutenberg.org/files/1342/1342-h/1342-h.htm'
Emma = 'https://www.gutenberg.org/files/158/158-h/158-h.htm'

def word_freq(URL):
    '''
    returns the frequency distribution of the text found at URL
    
    word_freq: Str -> (dictof Str (Nat))
    '''
    # extract text by fetching URL and creating beautiful soup
    r = requests.get(URL)
    r.encoding = 'utf-8'
    html = r.text
    soup = BeautifulSoup(html, features="lxml")
    text = soup.get_text()
    
    # create a list of the words 
    tokenizer = nltk.tokenize.RegexpTokenizer('\w+')
    tokens = tokenizer.tokenize(text)
    
    # create a list where all the words are in lowercase
    words = []
    for word in tokens:
        words.append(word.lower())
    
    # create a new list without stop words
    nltk.download('stopwords')   
    sw = stopwords.words('english') + ['would', 'could', 'may', 'might', 'must']
    new_words = []
    for word in words:
        if word not in sw:
            new_words.append(word)
    
    # create and return the frequency distribution        
    freqdist = nltk.FreqDist(new_words)
    return freqdist

def compare_freq(URL1, URL2):
    '''
    returns the plot of the 25 most common words in URL1 and URL2 vs word 
    frequency by calling word_freq()
    
    compare_freq: Str Str -> Plot
    '''
    # call word_freq(URL) to get the frequency distribution for each URL 
    one = word_freq(URL1)
    two = word_freq(URL2)
    
    # make a list containing the 25 most common in each novel
    words = []
    for x in one.most_common(25):
        words.append(x[0])
    for x in two.most_common(25):
        if x[0] not in words:
            words.append(x[0])
    
    # make a dictionary of type where the common words are the keys and the 
    # values are a list containing the frequency in the first and second URL
    wordd = {}
    for w in words:
        if w in one and w in two:
            wordd[w] = [one[w], two[w]]
        elif w in one and w not in two:
            wordd[w] = [one[w], 0]
        elif not w in one and w in two:
            wordd[w] = [0, two[w]]        
        else:
            wordd[w] = [0,0] 
    
    # find the titles
    r1 = requests.get(URL1)
    r1.encoding = 'utf-8'
    html1 = r1.text
    soup1 = BeautifulSoup(html1, features="lxml")
    title1 = soup1.find('title')
    
    r2 = requests.get(URL2)
    r2.encoding = 'utf-8'
    html2 = r2.text
    soup2 = BeautifulSoup(html2, features="lxml")
    title2 = soup2.find('title')    
    
    # create a dataframe
    df = pd.DataFrame.from_dict(wordd).T
    df.columns = [title1, title2]
    
    # return bar graph
    return df.plot(kind = 'bar')


compare_freq(Emma, PandP)