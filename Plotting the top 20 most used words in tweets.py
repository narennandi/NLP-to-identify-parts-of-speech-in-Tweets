import pip
#installing twitter library and textblob library
pip.main(['install','twitter'])
pip.main(['install','textblob'])

#importing TextBlob Library to perform NLP techniques
from textblob import TextBlob
!python -m textblob.download_corpora

#importing twitter packages
from twitter import Twitter
from twitter import OAuth
from twitter import TwitterHTTPError
from twitter import TwitterStream

#import numpy, pandas and json_normalize
import numpy as np
import pandas as pd
from pandas.io.json import json_normalize

#Twitter keys
#Create your own access tokens by going to the url below
#https://developer.twitter.com/en/docs/basics/authentication/guides/access-tokens.html
ck = "gwEdUQjvo9JDSLMpii205Q06O"
cs = "OlA4PIlLfpZ5HcEAGPOIJx4DwduhmACShoGQ66mJYt4ocxShwX"
at = "823996990329589760-1wW34frljiy7HrWp777qGFzOhEZksMW"
ats = "nzbKJCBUqlCsP6MNe5CFrOzZHo4wcvbubt1nJTqRkvFiB"

# Twitter uses OAuth to provide Authorized access to its API 
oauth = OAuth(at,ats,ck,cs)

#Twitter search
api = Twitter(auth=oauth)

#Assigning "Cavaliers" to the Variable q
q='Cavaliers'

#Creating a New Dataframe using pandas
df = pd.DataFrame()

#Assigning value Zero to Variable Mid
mid = 0

#building logic to extract 1000 tweets because it can only extract 100 at a time
for i in range(10):
    if i==0:
        search_result = api.search.tweets(q=q, count = 100)
    else:
        search_result = api.search.tweets(q=q, count=100, max_id=mid)
        #In the above line mid is assigned to max_id since mid has the 1 id less than the least mid
        #from the previously pulled data
    #Normalizing values in the Statuses section of search_result and storing it in dftemp
    dftemp = json_normalize(search_result,'statuses')
    #taking the minimum value in the id column and storing it in mid
    mid = dftemp['id'].min()
    #In order to make sure we do not pull out the same tweets we use the (mid=mid - 1) logic since
    #every tweet has an individual id
    mid = mid - 1
    #appending the df data frame with the values stored in dftemp
    df = df.append(dftemp, ignore_index = True)

#Viewing the number of rows and columns that are present
df.shape

#Storing all the tweets in the column Text in the variable tweettext
tweettext = df['text']

#Creating a new dataframe using Pandas and storing it in the variable wordlist
wordlist = pd.DataFrame()

#Creating a for loop
for t in tweettext:
    #performing textblob of t which is the tweets present in tweettext
    tx = TextBlob(t)
    #creating an empty list named ww
    ww = []
    #tx.tags assigns tags to all the words in the tweets
    for word, tag in tx.tags:
        # Checking if Tags belong to a noun(singular), noun(plural), proper noun(singular), proper noun(plural) 
        if tag in ('NN', 'NNS', 'NNP', 'NNPS'):
        #Lemmatize groups different forms of a word so that they can be analyzed as a single item 
        #Here, after lemmatizing it appends the words in the empty list ww
           ww.append(word.lemmatize())
    #Since the length of the list ww would not be equal to zero anymore, 
    #it will append all the data from ww in the empty dataframe "wordlist"          
    if len(ww) !=0:
        wordlist = wordlist.append(ww, ignore_index=True)

#Using the groupby function to visualize how many similar words are grouped and storing it in Allword         
allword = wordlist.groupby(0).size()

#Sorting values in Descending Order, selecting the top 20 words and storing it in top20allword
top20allword = allword.sort_values(0,ascending=False).head(20)

#plotting a bar chart to showcase the top20 words from all the tweets
top20allword.plot(kind='bar',title='Top 20 words')
