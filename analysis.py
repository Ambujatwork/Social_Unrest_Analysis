import pandas as pd
from textblob import TextBlob
import re

# df = pd.read_csv('tweets.csv')
# data = df['tweet']

class TweetAnalyzer():
    def clean_tweet(self,tweet):
        result = ' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
        print(result,'\n')
        return result#' '.join(re.sub("(@[A-Za-z0-9]+)|([^0-9A-Za-z \t])|(\w+:\/\/\S+)", " ", tweet).split())
    def analysis_sentiment(self, tweet):
        analysis = TextBlob(self.clean_tweet(tweet))
        
        if analysis.sentiment.polarity > 0:
            return 1
        elif analysis.sentiment.polarity == 0:
            return 0
        else:
            return -1
    
    def social_unrest_evaluate(self,data_synthesized,sentiments,negativity):
        keywords = ['deadly','riots','civil war','burning','religion','protest', 'anti-government','government','resign','resignation']
        keyword_counts = {keyword: 0 for keyword in keywords}
        total = 0
        
        # Iterate through each sentence
        for i in range(len(data_synthesized)):
            if sentiments[i]==-1:
                words = data_synthesized[i].split()    
                # Count the occurrences of each keyword in the sentence
                for keyword in keywords:
                    if keyword in words:
                        keyword_counts[keyword] += 1
                        total+=1
        for keyword, count in keyword_counts.items():
            print(f"'{keyword}' appears {count} times.")
        keyword_factor = total/sentiments.count(-1)
        print(f"keyword factor: {keyword_factor}")
        total_prob = negativity+ keyword_factor
        if negativity<0.20:
            print("1")
            # return (1,negativity)
            return(1,total_prob)

        elif .20<total_prob<=.40:
            print(0)
            return (0,total_prob)
        else:
            print(-1)
            return (-1,total_prob)
    

# if __name__=='__main__':
#     tweet_analysis = TweetAnalyzer()
#     data_synthesized = [tweet_analysis.clean_tweet(tweet) for tweet in data]
#     sentiments = [tweet_analysis.analysis_sentiment(tweet) for tweet in data]
#     print(f"1: {sentiments.count(1)}, 0: {sentiments.count(0)}, -1: {sentiments.count(-1)}")
#     negativity = sentiments.count(-1)/(sentiments.count(1)+sentiments.count(-1))
#     if negativity<0.20:
#         print("There is no chances of social unrest")
#     else:
#         tweet_analysis.social_unrest_evaluate(data_synthesized,sentiments,negativity)