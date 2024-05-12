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
   
    text.append(f['rawContent'])
    scores = analyzer.polarity_scores(f['rawContent'])

    if scores["compound"] >= 0.05:
        label.append(2) #pos
    elif scores["compound"] <= -0.05:
        label.append(1) #neg
    else:
        label.append(0) #neu
    
data = {
    "text": text,
    "label": label
}
    
df = pd.DataFrame(data)
print(df)