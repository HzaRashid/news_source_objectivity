import re
import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob as TB, Word
import numpy as np
import pandas as pd
import tweepy as ty
import streamlit as st
from plotly import graph_objs as go


# get twitter developer credentials
twitter_info = pd.read_csv('keys_tokens.csv')

consumer_key = twitter_info['API Key'][0]
consumer_secret = twitter_info['API Key Secret'][0]
access_token = twitter_info['Access Token'][0]
access_token_secret = twitter_info['Access Token Secret'][0]

# authorize credentials to get access to Twitter API
auth = ty.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = ty.API(auth, wait_on_rate_limit=True)

st.header('Objectivity of News Source \n From last 500 tweets')

# map name of source to its twitter handle
news_sources = {'Reuters': 'Reuters',
                'New York Times': 'nytimes',
                'Wall Street Journal': 'WSJ',
                'The Associated Press': 'AP',
                'CNN': 'CNN',
                'NBC': 'NBCNews',
                'Fox News': 'FoxNews',
                'BBC': 'BBCBreaking',
                'Al Jazeera (English)': 'AJEnglish'
                }

user_choice_source = st.selectbox('Select News Source', news_sources.keys())
st.write('The Objectivity Score ranges from 0% to 100%, \
         from Subjective to Objective, respectively.')
twitter_handle = news_sources.get(user_choice_source)

# download necessary files to use nltk, textblob, and vader
nltk.download('omw-1.4')
nltk.download('wordnet')
nltk.download('vader_lexicon')


@st.cache(show_spinner=False)
def clean_tweet(text):

    tweet = text
    to_replace = ['@[\w]+', 'RT[\s]+', '[^\w]', '#', 'http[\w]+']

    # remove @ mentions, RTs, hashtags ...
    for character_sequence in to_replace:
        tweet = re.sub(character_sequence, '', tweet)

    # turn words into most basic form
    tweet = ' '.join(Word(word).lemmatize() for word in tweet.split())

    return tweet


sia = SentimentIntensityAnalyzer()


def objectivity_scores(tweet):

    textblob_objectivity = 1 - TB(tweet).sentiment.subjectivity
    vader_neutrality = sia.polarity_scores(tweet).get('neu')
    avg_objectivity = (textblob_objectivity + vader_neutrality) / 2

    return textblob_objectivity, vader_neutrality, avg_objectivity


@st.cache(show_spinner=False, allow_output_mutation=True)
def get_tweets_data():

    query = ty.Cursor(api.user_timeline, screen_name=twitter_handle, tweet_mode='extended').items(500)

    tweet_text, date_posted = [], []
    for tweet in query:
        tweet_text.append(tweet.full_text)
        date_posted.append(tweet.created_at)

    tweets = pd.DataFrame()
    tweet_column = 'Tweets'

    tweets.insert(loc=0, column=tweet_column, value=tweet_text)
    tweets.index = date_posted
    tweets.reset_index()

    tweets[tweet_column] = tweets[tweet_column].apply(clean_tweet)

    o_scores = [objectivity_scores(tweet) for tweet in tweets[tweet_column]]

    tb_scores, vdr_scores, avg_scores = [], [], []
    for tb_score, vdr_score, avg_score in o_scores:
        tb_scores.append(tb_score)
        vdr_scores.append(vdr_score)
        avg_scores.append(avg_score)

    # the objectivity score ranges between 0 and 1
    # 0 means the tweet is completely subjective
    # 1 means the tweet is completely objective
    tweets['TextBlob Objectivity Scores'] = tb_scores
    tweets['Vader Neutrality Scores'] = vdr_scores
    tweets['Average Objectivity Scores'] = avg_scores

    return tweets


# load tweet data of news source
load_data_state = st.text('loading data...')
news_source_tweets = get_tweets_data()
load_data_state.text('')

st.subheader('Tweet Data of ' + user_choice_source)


def plot_objectivity_scores():
    fig = go.Figure([
        go.Scatter(
            x=news_source_tweets.index,
            y=news_source_tweets['Average Objectivity Scores'].rolling(100, min_periods=5).mean()*100,
            name='Objectivity Scores (Taken from Average)',
            mode='lines',
            line=dict(color='#088F8F')
        )
    ])
    fig.layout.update(
        title_text='100 Tweets MA of Objectivity',
        xaxis_title='Date',
        yaxis_title='Objectivity Score',
        xaxis_rangeslider_visible=True
    )
    return fig


# show plot of objectivity scores
st.plotly_chart(plot_objectivity_scores())

# calculate average/mean objectivity score
mean_objectivity_scores = list(news_source_tweets['Average Objectivity Scores'])
mean_objectivity = np.mean(mean_objectivity_scores)

st.subheader('Mean Objectivity Score: ' + str(mean_objectivity*100)[:5] + '%')

# show raw data (DataFrame of tweets & objectivity scores)
st.subheader('Raw Data')
st.write(news_source_tweets)
st.write("The values under the 'Average Objectivity Scores' (AOS) column are taken \
         from the average of the TextBlob and Vader columns. \
         \n The data from AOS is used for the above chart, and calculating \
          the 'Mean Objectivity Score'.")

if __name__ == '__main__':
    twitter_handle='Reuters'
    data = get_tweets_data()
    print(data)