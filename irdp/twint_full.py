import twint
from wordcloud import WordCloud
import re
import pandas as pd
import numpy as np
import nest_asyncio
import seaborn as sns
import matplotlib.pyplot as plt
import cv2
import nltk
from nltk.probability import FreqDist
nest_asyncio.apply()

# Cleaning Tweets
def cleanTweets(text):
    text = re.sub("[^a-zA-Z0-9]", " ", text)
    return text

def Lowercase(lowercase):
  lowercase = lowercase.lower()
  return lowercase

# Extra tweets from keyword search
def ExtractTweets(search_list,Limit,Date_since,Date_until):
  try:
    for search in search_list:
        #Extract tweets
        a = twint.Config()
        a.Limit = Limit
        # Extract tweets since and until date
        a.Since = Date_since
        a.Until = Date_until
        #a.Hideoutput = True
        search_filter = ['','501Awani ','UMonline ', 'bharianmy ']
        sentence1 = '-from:'.join(search_filter)
        a.Search = search + sentence1
        a.Count = True
        a.Pandas = True
        a.Custom['tweet1'] = ["tweet"]

        #Run
        print("Printing tweets from search_list")
        twint.run.Search(a)
        return twint.storage.panda.Tweets_df['tweet'].to_frame()
  except:
    user1 =  pd.DataFrame()
    user1['tweet']=['none']
    return  user1
 
#Extra Tweets from specific user 
def tweetsExtractor(username_list,Limit,Date_since,Date_until):
  try:
    for username in username_list:
        # Configure
        b = twint.Config()
        # Load username from usernames list below
        b.Username = username
        # exclude replies
        #b.Search = "exclude:replies"
        # set search since date
        b.Since = Date_since
        b.Until = Date_until
        b.Limit = Limit
        b.Count = True
        b.Pandas = True
        b.Custom['tweet2'] = ["tweet"]
 
        # Run
        print("Downloading %s's tweets:" % username)
        twint.run.Search(b)
        return twint.storage.panda.Tweets_df['tweet'].to_frame()
  except:
    mps =  pd.DataFrame()
    mps['tweet']=['none']
    return  mps

def tweetsExtract(news_list,Limit,Date_since,Date_until,search_list):
  test =  pd.DataFrame()
  test['tweet']=['none']
  for news in news_list:
    try:
          # Configure
          c = twint.Config()
          # Load username from usernames list below
          c.Username = news
          c.Search = search_list
          # set search since date
          c.Since = Date_since
          c.Until = Date_until
          c.Limit = Limit
          c.Count = True
          c.Pandas = True
          c.Custom['tweet3'] = ["tweet"]
  
          # Run
          print("Downloading %s's tweets:" % news)
          twint.run.Search(c)
          tmp = twint.storage.panda.Tweets_df['tweet'].to_frame()
          test.append(tmp)
    except:
      continue
  return test

def tokenize(text):
  tokens = re.split("\W+", text)
  return tokens

def remove_stopword(text,stopwords):
  text_nostopword= [char for char in text if char not in stopwords]
  return text_nostopword  

def main_bulk(Date_since,Date_until,Limit,searchword,mpsuser):
    search_list = [searchword]
    user = ExtractTweets(search_list,Limit,Date_since,Date_until)
    usernames_list = [mpsuser] 
    kuning = tweetsExtractor(usernames_list,Limit,Date_since,Date_until)
    news_list = ['bharianmy', 'UMonline', 'staronline'] 
    merah = tweetsExtract(news_list,Limit,Date_since,Date_until,search_list)

    biru = user.copy()
    for row in user.itertuples():
        user.at[row.Index, 'tweet',] = cleanTweets(row.tweet)
    for row in kuning.itertuples():
        kuning.at[row.Index, 'tweet',] = cleanTweets(row.tweet)
    for row in merah.itertuples():
        merah.at[row.Index, 'tweet',] = cleanTweets(row.tweet)

    for row in user.itertuples():
        user.at[row.Index, 'tweet',] = Lowercase(row.tweet)
    for row in kuning.itertuples():
        kuning.at[row.Index, 'tweet',] = Lowercase(row.tweet)
    for row in merah.itertuples():
        merah.at[row.Index, 'tweet',] = Lowercase(row.tweet)

    user.replace(r'^\s*$', np.nan, inplace=True, regex=True)
    user.dropna(how="any", axis=0, inplace=True)
    kuning.replace(r'^\s*$', np.nan, inplace=True, regex=True)
    kuning.dropna(how="any", axis=0, inplace=True)
    merah.replace(r'^\s*$', np.nan, inplace=True, regex=True)
    merah.dropna(how="any", axis=0, inplace=True)

    # Removing tweets that has less than 3 character
    user["tweet"]= user["tweet"].apply(lambda x: " ".join ([w for w in x.split() if len (w)>3]))
    kuning["tweet"]= kuning["tweet"].apply(lambda x: " ".join ([w for w in x.split() if len (w)>3]))
    merah["tweet"]= merah["tweet"].apply(lambda x: " ".join ([w for w in x.split() if len (w)>3]))
    user['tweet']= user['tweet'].apply (lambda x: tokenize(x))
    kuning['tweet']= kuning['tweet'].apply (lambda x: tokenize(x))
    merah['tweet']= merah['tweet'].apply (lambda x: tokenize(x))

    #Stopword remove
    f = open("irdp/EnglishMalay-stopwords.txt", 'r')
    stopwords = f.read().split()

    user['tweet']= user['tweet'].apply(lambda x: remove_stopword(x,stopwords))
    kuning['tweet']= kuning['tweet'].apply(lambda x: remove_stopword(x,stopwords))
    merah['tweet']= merah['tweet'].apply(lambda x: remove_stopword(x,stopwords))

    # Put into a list
    data_list = user.loc[:,"tweet"].to_list()
    data_list_user = user.loc[:,"tweet"].to_list()
    data_list_kuning = kuning.loc[:,"tweet"].to_list()
    data_list_merah = merah.loc[:,"tweet"].to_list()

    # Put into flat list
    flat_data_list = [item for sublist in data_list for item in sublist]
    flat_data_list_user = [item for sublist in data_list_user for item in sublist]
    flat_data_list_kuning = [item for sublist in data_list_kuning for item in sublist]
    flat_data_list_merah = [item for sublist in data_list_merah for item in sublist]

    # Count the word frequency
    data_count= pd.DataFrame(flat_data_list)
    data_count= data_count[0].value_counts()
    data_count_user= pd.DataFrame(flat_data_list_user)
    data_count_user= data_count_user[0].value_counts()
    data_count_kuning= pd.DataFrame(flat_data_list_kuning)
    data_count_kuning= data_count_kuning[0].value_counts()
    data_count_merah= pd.DataFrame(flat_data_list_merah)
    data_count_merah= data_count_merah[0].value_counts()

    freq_count = FreqDist()
    for words in data_count:
        freq_count[words] +=1
        freq_count
    freq_count = FreqDist()
    for words in data_count_user:
        freq_count[words] +=1
        freq_count
    for words in data_count_kuning:
        freq_count[words] +=1
        freq_count
    for words in data_count_merah:
        freq_count[words] +=1
        freq_count

    #pd.set_option('display.max_row', None)
    from collections import OrderedDict
    from collections import Counter # For adding two or more dictionary values into one
    dictionary_user = data_count_user.to_dict(into=OrderedDict) #change to object use ordereddict
    dict_limit_user = OrderedDict(Counter(dictionary_user).most_common(10))

    dict_set_user = set(dict_limit_user.keys())

    dictionary_merah = data_count_merah.to_dict(into=OrderedDict) #change to object use ordereddict
    dictionary_kuning = data_count_kuning.to_dict(into=OrderedDict) #change to object use ordereddict

    #Limit dict
    Dict_merahlim = {key:dictionary_merah[key] for key in set(dictionary_merah) & dict_set_user}
    Dict_kuninglim = {key:dictionary_kuning[key] for key in set(dictionary_kuning) & dict_set_user}

    Dict_user = Counter(dict_limit_user)
    Dict_merah = Counter(Dict_merahlim)
    Dict_kuning = Counter(Dict_kuninglim)

    add_dict = Dict_user + Dict_merah + Dict_kuning
    Dict_purple = dict(add_dict)
    Dict_purple # sum of all Dict

    # Division MPs
    Dict_user_rat = {k: (Dict_user[k])/Dict_purple[k] for k in Dict_user}
    Dict_user_percent = {k: Dict_user_rat[k]*100 for k in Dict_user_rat}

    #Scoring
    # create graph for dictionary
    Dict_user_percent
    keys = list(Dict_user_percent.keys())
    # get values in the same order as keys, and parse percentage values
    vals = [float(Dict_user_percent[k]) for k in keys]
    plt.figure(figsize=(10,5))
    sns.barplot(x=keys, y=vals, alpha=0.8)
    plt.title('Top Words Overall')
    plt.ylabel('Word from Tweet', fontsize=12)
    plt.xlabel('Percentage correlation', fontsize=12)
    plt.savefig('irdp/output1.png')    
    plt.close()

    #Graph keyword
    freq_count = FreqDist()
    for words in data_count:
        freq_count[words] +=1
        freq_count

    data_count = data_count[:20,]
    plt.figure(figsize=(10,5))
    sns.barplot(data_count.values, data_count.index, alpha=0.8)
    plt.title('Top Words Overall')
    plt.ylabel('Word from Tweet', fontsize=12)
    plt.xlabel('Count of Words', fontsize=12)
    plt.savefig('irdp/output2.png')   
    plt.close()

    #Wordcloud, removed some recolor code to reduce runtime
    mask = cv2.imread('irdp/twitter.png')
    wcloud = WordCloud(collocations=False,mask=mask,background_color='white',stopwords=stopwords,colormap='viridis').generate(' '.join(biru['tweet']))
    wcloud.to_file('irdp/output.png')