import re
import pandas as pd
import tweepy as ty
import streamlit as st
import nltk
from nltk.corpus import stopwords
from textblob import TextBlob as TB, Word
from plotly import graph_objs as go
from nltk.sentiment.vader import SentimentIntensityAnalyzer

twitter_info = pd.read_csv('keys_tokens.csv')

consumer_key = twitter_info['API Key'][0]
consumer_secret = twitter_info['API Key Secret'][0]
access_token = twitter_info['Access Token'][0]
access_token_secret = twitter_info['Access Token Secret'][0]

auth = ty.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = ty.API(auth, wait_on_rate_limit=True)

st.header('Objectivity of News Source \n From last 500 tweets')

# map name of source to its twitter handle
news_sources = {'New York Times': 'nytimes',
                'Wall Street Journal': 'WSJ',
                'Fox News': 'FoxNews',
                'CNN': 'CNN',
                'BBC': 'BBC',
                'Al Jazeera': 'AJEnglish'}

user_choice_source = st.selectbox('Select News Source', news_sources.keys())
twitter_handle = news_sources.get(user_choice_source)


@st.cache
def clean_tweet(text):
    nltk.download('wordnet')
    nltk.download('stopwords')
    common_words = stopwords.words('english')

    tweet = text
    to_replace = ['@[\w]+', 'RT[\s]+', '[^\s\w]', '#', 'http[\w]+']

    # remove keyword, @ mentions, RTs, ...
    for character_sequence in to_replace:
        tweet = re.sub(character_sequence, '', tweet)

    # remove words that have no impact on sentiment measure
    tweet = ' '.join(word for word in tweet.split() if word not in common_words)

    # turn words into most basic form
    tweet = ' '.join(Word(word).lemmatize() for word in tweet.split())

    return tweet


sia = SentimentIntensityAnalyzer()


def objectivity_scores(tweet):

    textblob_objectivity = 1 - TB(tweet).sentiment.subjectivity
    vader_objectivity = sia.polarity_scores(tweet).get('neu')
    avg_objectivity = (textblob_objectivity + vader_objectivity) / 2

    return textblob_objectivity, vader_objectivity, avg_objectivity


@st.cache(show_spinner=False)
def get_tweets_data():

    query = ty.Cursor(api.user_timeline, screen_name=twitter_handle, tweet_mode='extended', lang='en').items(50)

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
    tweets['Vader Objectivity Scores'] = vdr_scores
    tweets['Average Objectivity Scores'] = avg_scores

    return tweets


news_source_tweets = get_tweets_data()
st.subheader('Tweet Data of New York Times')
print(news_source_tweets.index)
st.write(news_source_tweets.tail())


def plot_objectivity_scores():
    fig = go.Figure([
        go.Scatter(

            x=news_source_tweets.index,
            y=news_source_tweets['TextBlob Objectivity Scores'],
            name='TextBlob Objectivity Score',
            mode='lines',
            line=dict(color='#088F8F')
        ),
        go.Scatter(
            x=news_source_tweets.index,
            y=news_source_tweets['Vader Objectivity Scores'],
            name='Vader Objectivity Scores',
            mode='lines',
            line=dict(color='#F08080')
        ),
        go.Scatter(
            x=news_source_tweets.index,
            y=news_source_tweets['Average Objectivity Scores'],
            name='Average Objectivity Scores',
            mode='lines',
            line=dict(color='black')
        )

    ])
    fig.layout.update(
        title_text='Actual and Predicted Prices ($USD)',
        xaxis_title='Date',
        yaxis_title='Objectivity Score',
        xaxis_rangeslider_visible=True
    )
    return fig



st.plotly_chart(plot_objectivity_scores())