import json
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import os.path

nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()
path="C:/Users/Frank/anaconda3/envs/py10/Lib/site-packages/twscrape/Player scrapes/TS_DRTG"
scorelist=[]

for filename2 in os.listdir(path):
    file1 = open(os.path.join(path,filename2), 'r')

    Lines = file1.readlines()

    label=[]
    text=[]
    total_pos=0
    line_count=0
    for line in Lines:
        f = json.loads(line)
    
        text.append(f['rawContent'])
        line_count=line_count+1
        scores = analyzer.polarity_scores(f['rawContent'])

        if scores["neg"] > scores["pos"]:
            label.append(0)
        else:
            label.append(1)
            total_pos=total_pos+1
        
    data = {
        "text": text,
        "label": label
    }
        
    #df = pd.DataFrame(data)
    #print(df)
    scorelist.append(total_pos/line_count)

print(scorelist)