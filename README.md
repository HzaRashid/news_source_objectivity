# news_source_objectivity
#### Find a news source's twitter account, calculate the objectivity of each of its last 500 tweets, and calculate the average objectivity of those tweets.



#### The visualization can be found [here](https://share.streamlit.io/hzarashid/news_source_objectivity/main/twitter_objectivity.py)




### In depth:
##### [twitter_objectivity.ipynb](https://github.com/HzaRashid/news_source_objectivity/blob/main/twitter_objectivity.ipynb) is where most of the rough the work was done, to learn how to gather the tweets and 'clean' them (i.e., remove @ mentions, hashtags). The code on which the visualization runs is located in  [twitter_objectivity.py](https://github.com/HzaRashid/news_source_objectivity/blob/main/twitter_objectivity.py)


##### To access tweets in real time, a [Twitter Developer](https://developer.twitter.com/en) account needs be made with an application for 'Elevated Access'. After which, four unique authorization credentials will be given; 'API Key', 'API Key Secret', 'Access Token', and 'Access Token Secret'. Authorizing these credentials using the tweepy library will give access to the Twitter API, which gives access to tweets.

#### To measure the objectivity of a tweet, I used the [TextBlob and Vader libraries](https://towardsdatascience.com/sentiment-analysis-vader-or-textblob-ff25514ac540), which process textual data. 

- TextBlob provides a measure of polarity (feeling, not as relevant to this project), and more importantly, subjectivity. 
- TextBlob's subjectivity score ranges from 0 to 1, where 0 indicates the text is completely objective and 1 indicates the opposite. Subtracting this value from 1 will (roughly) yield TextBlob's measure of objectivity (i.e., objectivity score = 1 - subjectivity score), where now a score of 0 indicates the tweet is completely subjective, and a score of 1 indicates a completely objective tweet. This is relevant to how Vader performs sentiment analysis of a text.

 - Vader provides a measure of positivity, negativity, and neutrality of a piece of text, as well as a normalized sum of those metrics, called the 'Compound score'.  The metric relevant to this project is the Neutral emotion Score, which is expressed as a percentage, with 0 indicating a completely emotional piece of text, and 1 indicating the opposite. 
 
 - So both TextBlob and Vader's measure of objectivity and neutral emotion range between 0 and 1, respectively.
 - As a result, in this project, I calculated the objectivity of a tweet by taking the average of TextBlob's score of objectivity and Vader's score of neutral emotion.

- Important to note: neither TextBlob nor Vader are completely accurate – the data in this project is meant to provide a rough estimate of objectivity.
