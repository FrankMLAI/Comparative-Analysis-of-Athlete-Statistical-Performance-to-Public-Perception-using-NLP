import json
import nltk
import pandas as pd
from nltk.sentiment.vader import SentimentIntensityAnalyzer

nltk.download("vader_lexicon")
analyzer = SentimentIntensityAnalyzer()

file1 = open('test2.txt', 'r')
Lines = file1.readlines()

label=[]
text=[]
for line in Lines:
    f = json.loads(line)

    #print ("\n NEW TWEET HERE: \n")
    #print(f['rawContent'])    
    text.append(f['rawContent'])
    scores = analyzer.polarity_scores(f['rawContent'])

    if scores["neg"] > scores["pos"]:
        label.append(0)
    else:
        label.append(1)
    
data = {
    "text": text,
    "label": label
}
    
df = pd.DataFrame(data)
print(df)