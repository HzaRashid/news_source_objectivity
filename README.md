# news_source_objectivity
#### Find a news source's twitter account, calculate the objectivity of each of its last 500 tweets, and calculate the average objectivity of those tweets.

### update:
#### Due to an update to Twitter's Developer API made earlier this year, those with free access (including myself) are no longer able to query tweets. So the visualization component of this project is no longer available. 
#### for more details: [see here](https://twittercommunity.com/t/understanding-the-error-453-you-currently-have-access-to-a-subset-of-twitter-api-v2-endpoints/200361) and [here](https://twittercommunity.com/t/understanding-the-error-453-you-currently-have-access-to-a-subset-of-twitter-api-v2-endpoints/200361)


### In depth:
If still interested, The code on which the visualization used to run is located in  [twitter_objectivity.py](https://github.com/HzaRashid/news_source_objectivity/blob/main/twitter_objectivity.py)

#### To measure the objectivity of a tweet, I used the [TextBlob and Vader libraries](https://towardsdatascience.com/sentiment-analysis-vader-or-textblob-ff25514ac540), which process textual data. 

- TextBlob provides a measure of polarity (i.e., tone, feeling), and subjectivity. 
- TextBlob's subjectivity score ranges from 0 to 1, where 0 indicates the text is completely objective and 1 indicates the opposite. Subtracting this value from 1 will (roughly) yield TextBlob's measure of objectivity (i.e., objectivity score = 1 - subjectivity score), where now a score of 0 indicates the tweet is completely subjective, and a score of 1 indicates a completely objective tweet. This is relevant to how Vader performs sentiment analysis of a text.

 - Vader provides a measure of positivity, negativity, and neutrality of a piece of text, as well as a normalized sum of those metrics, called the 'Compound score'.  The metric relevant to this project is the Neutral emotion Score, which is expressed as a percentage, with 0 indicating a completely emotional piece of text, and 1 indicating the opposite. 
 
 - So both TextBlob and Vader's measure of objectivity and neutral emotion range between 0 and 1, respectively.
 - As a result, in this project, I calculate the objectivity of a tweet by taking the average of TextBlob's score of objectivity and Vader's score of neutral emotion.

- Important to note: neither TextBlob nor Vader are completely accurate – this project is experimental.
