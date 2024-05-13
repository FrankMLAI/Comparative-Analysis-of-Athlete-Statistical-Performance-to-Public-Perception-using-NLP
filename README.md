## Introduction
The debate of “who is the best?” is a discussion topic that is as old as time. With the introduction of online spaces for discourse, humans have migrated their battlefields of debate onto the internet. Nowadays it is not uncommon to observe the most discussed topics and notice that at the top of them are not politics or sciences, but rather sports figures, many of whom are Basketball players. Nevertheless, since discussion platforms, such as X (Twitter) or Threads, support freedom of speech, any individual is permitted to say anything, regardless of factual accuracy. As a result, individuals can openly slander or spread hate regarding players who statistically do not deserve such criticism. Nevertheless, with the advent of NLP, we can construct a mechanism to “fact check” the overall sentiments regarding players’ performances and distinguish those who are saying the truth from those who are only trying to spread hate. Utilizing sentiment analysis with a popular discussion platform, we can ascertain the general sentiment regarding a player’s performance and then compare it to the player’s statistics on basketball reference to see if there is a discrepancy between perceived performance and actual performance. We can then draw conclusions on whether a player is currently overrated or over-hated and bring more clarity and veracity to the world of sports discussions. 

## Problem Statement
The objective of our project is to design a model for performing sentiment analysis on online sports discussions, namely NBA discourse on X, and perform fact checking by cross referencing the actual statistics on Basketball-Reference.

## Data Collection
We had one method for collecting data, as well as a source for a large dataset to train our model on. Our method for collecting data involved using an open-source X scraper, originally made for twitter. Due to the recent purchase of X by Elon Musk the ease of scraping twitter has gotten stricter, making many other scraping options unavailable. This method of scraping involves downloading a repository from GitHub called Twscrape, and running the code with user made twitter accounts to collect information [13]. This tool has two data models, user and tweet, and it allows the user to work around the restrictions and limits set after July 21, which included the following behaviors:	
1.	All restrictions are applied in 15 minute intervals.
2.	Request are limited to 50 searches per account
With the tool, API calls are made requesting a search provided by the user. These searches can be further filtered using specific prompts. Within the GitHub readme for Twscrape is a link to another GitHub page for phrases to use for advanced searches. As we progressed with our project, we eventually added more specific criteria to our search queries, such as defense or shooting ability, to access those areas of a player’s skillset as well.

The other large source of data that was used exclusively for training the BERT model is sentiment140. Sentiment140 consists of Twitter messages with emoticons, which are used as noisy labels for sentiment classification. This dataset is provided from a variety of sources including Kaggle, Hugging Face, and Tensorflow. The dataset consists of 1.6 million tweets, consisting of 560,639 negative and 559,361 positive tweets. The only columns used for training the BERT model were the text and sentiment scores, which were marked 0 for negative or 4 for positive. 

Lastly, for our source of ground truth, we would scrape Basketball-Reference for statistics, as it is the most comprehensive source of basketball player data spanning from 1947 to the present day. It not only provides the common counting stats that most basketball data sources have, but advanced stats derived from the box scores from each game, such as BPM (box-plus-minus), TS% (true shooting percentage), and DRTG (defensive rating). We believe that these will be key stats to correlate with sentiments (more detail in the methodologies section). The basketball_reference_scraper was used to scrape the site, accessing advanced game logs to access the desired statistics.

## Data Preprocessing
For the sentiment140 dataset, a small amount of preprocessing was performed to prepare the
data for training the BERT model. The values were first checked for missing values, unused columns were removed, sentiment scores were changed to 0 for negative and 4 for positive. Lastly, the content of the tweet went through some cleaning to handle any html content, empty spaces, or any characters that were not letters, numbers, or punctuation. 

The scraped outputs from basketball_reference_scraper were aggregated into a folder scheme that separated the logs by player. The filenames were the dates of the games. In doing so, we are able to match the game logs with the sentiments, as both utilize the players’ names and dates as identifying parameters. Next, the Tweet scrapes were parsed. Recognizing that each output Tweet line was its own JSON object, we loaded the scrapes using the JSON library and extracted the contents of the tweet, which were stored under “rawContent”.

Using Vader, a lexicon and rule-based sentiment tool that is specifically attuned to sentiments expressed in social media, we labeled the contents of each tweet. Using the positive, negative, and neutral scores that Vader returned, we would assess which label to assign each Tweet. For the 2-class dataset, we would label for positivity or negativity and for the 3 class one, we included a neutral score. With each tweet labeled, we are able to compare against the model trained to the million tweets, which follows the same binary (or trinary) label scheme.

## Methodology
The model chosen for performing the sentiment analysis is BERT. BERT is a transformer model that has been trained on a large corpus of English text, self-supervised 
Our fine tuning parameters :
•	Optimizer Adam, learning rate = 2e-5
•	Sparse Categorical Cross Entropy
•	Used Accuracy as the model’s training metric 
•	Trained on 3 epochs
•	Used a max sequence length of 128

## Sports stats
Box Plus-Minus (BPM) aims to evaluate how much a player contributed when they are on the court. BPM incorporates box score performance, team performance and player position to rate how well a player performed above league average per 100 possessions. As a result, we decided to use BPM as our metric for measuring game performance.

Upon finishing our BPM analysis, we realized that we could add granularity to our search criteria by honing in on tweets that specifically involved a player’s shooting or defensive ability. The statistics that correspond to those aspects would be TS% (true shooting percentage) and DRTG (defensive rating). 

## Model Results
These results show the model’s performance against the dataset. In both cases, the model’s loss decreased while the accuracy increased, which is the desired trend from training. The validation accuracy was lower than the training accuracy, and the validation loss was higher than the training accuracy. This is to be expected, but it means that the model performed better on the training data over the validation set. The validation loss and accuracy have a slight trend in the wrong direction, which could indicate over fitting, or that more tuning is required for the model to perform better. 
After the models were trained, as seen above, they were both tried against the additional dataset provided by hugging face that had three classes. The models performed well against the dataset when the neutral classes were excluded but neither performed well with it included. The 3 Class Model only reached an accuracy of 60%, while the 2 Class Model reached an accuracy high of 61% when the threshold was set to 0.10 (Refer to methodology for explanation). Because both accuracies were far below the performance of the 2 Class Model, when classifying only 2 classes, we decided to drop the attempt to classify neutral classes and focused on only positive and negative sentiment scores. 

## Spearman Rank Results
### BPM and Sentiment Scores Tables for Sampled Games
| Player | Metric | G1 | G2 | G3 | G4 | G5 | G6 |
| --- | --- | --- | --- | --- | --- | --- | --- |
| Stephen Curry | BPM | 4.2 | -2.9 |	7.8 |	0.2 |	11.2 |	5.6 |
| Stephen Curry | Sentiment | 0.833 |	0.645 |	0.645 |	0.64 |	0.833 |	0.833 |
| Joel Embiid | BPM | 7.8 | N/A |	14.7 |	22.4 |	N/A |	N/A |
| Joel Embiid | Sentiment | 0.807 | N/A |	0.784 |	0.667 |	N/A |	N/A |
| Giannis Ante. | BPM | 16.9 |	-1.2 |	4 |	8.8 |	9.8 |	9.6 |
| Giannis Ante. | Sentiment | 0.73 |	0.729 |	0.73 |	0.73 |	0.73 |	0.645 |
| Tyrese Hali. | BPM | 16.9 |	11.1 |	5.7 |	11.9 |	15.2 | N/A |
| Tyrese Hali. | Sentiment | 0.691 |	0.742 |	0.615 |	0.742 |	0.902 |	N/A |
| Nikola Jokic | BPM | 27.7 |	22.2 |	6.3 |	N/A | 26.4  | N/A |	
| Nikola Jokic | Sentiment | 0.754 |	0.796 |	0.772 |	N/A |	0.557	| N/A |	
| Lebron James | BPM | 14.1 |	8.6 |	-4.3 |	9.1 |	1.2 |	6.8 |
| Lebron James | Sentiment | 0.567 |	0.548 |	0.53 |	0.576 |	0.576 |	0.545 |
| Luka Doncic | BPM | 12.2 |	6.7 |	17.3 |	N/A |	14.3 |	14.9 |
| Luka Doncic | Sentiment | 0.667 |	0.803 |	0.737 | N/A |	0.569 |	0.737 |
| Alperen Sengun | BPM | 7.9 |	-1.3 |	1.6 |	7.5 |	2.2 |	9.3 |
| Alperen Sengun | Sentiment | 0.833 |	0.645 |	0.645 |	0.64 |	0.833 |	0.833 |
| Shai Gilgeous-A. | BPM | 24.3 |	9.6 |	16.3 |	10.1 |	8.6 |	19.3 |
| Shai Gilgeous-A. | Sentiment | 0.806 |	0.69 |	0.772 |	0.702 |	0.557 |	0.75 |

### DRTG and Sentiment Score Plot
| Player | DRTG | DRTG Sentiment | TS% | TS% Sentiment | 
| --- | --- | --- | --- | --- |
| Stephen Curry | 121.5 |	0.714 |	0.656833 |	0.719 |
| Joel Embiid | 109 |	0.779 |	0.651 |	0.644 |
| Giannis Ante. | 112.5 |	0.667 |	0.651833 |	0.885 |
| Tyrese Hali. | 128.2 |	0.677 |	0.7086 |	0.787 |
| Nikola Jokic | 117 |	0.926 |	0.6232 |	0.75	|
| Lebron James | 117 |	0.607 |	0.6408 |	0.719 |
| Luka Doncic | 108.4 |	0.814 |	0.5968 |	0.886 |
| Alperen Sengun | 112 | 0.862 |	0.536667 |	0.846 |
| Shai Gilgeous-A. | 112.33 |	0.556 |	0.677667 |	0.66 |

## Conclusion
Relative to the other players’ positions, the only defensively overrated player was Nikola Jokic. Considering the sports context, such an assessment is accurate as Jokic’s team is good defensively, but he individually is not. Taking the merits of his team into consideration, it is understandable of how he might have claimed undue credit and become overrated. Giannis, Lebron, and Shai appeared to be underrated defensively. Giannis’ contextual situation is almost the opposite of Jokic’s: he is a good defender, but his team got worse defensively due to a roster change that they made during the offseason [7]. Shai’s underrated status also makes sense considering that he is a young superstar playing for a small market team (Oklahoma) without enough of a fanbase to properly assess him. Lebron’s underrated status could potentially be due to the opposite reason as Shai: he is too popular and that makes him a target for haters who will post negative sentiments regardless of Lebron’s actual performance.

While our results were able to illustrate insights into player assessment validity, it is important to acknowledge the limitations within the project. Our main issue would be sampling size with regards to the scraped Tweets. We believe that our results would be more decisive if we had access to a full season of Basketball Tweets to analyze. Working within the constraints of our scraper and X’s restrictions, we had to lower the sample size. 

Another classifier limitation is one that we foresaw but were unable to address. That is the issue of NBA discussion vernacular. As most tweets have casual prose, it will be necessary to scrape with queries that address slang, nicknames, and euphemisms to truly scrape out all relevant Tweets. Our format of searching by the player’s full name is quite limiting, considering that most discussions refer to players by their nicknames rather than their full names (people rarely attempt to type out “Giannis Antetokounmpo”). Furthermore, terms like “bucket” or “D” are slang terms that refer to scoring ability and defensive ability respectively but are not included in our queries. While these terms are important to recognize, creating a definitive list of them for querying is not feasible considering the informality of it all.
In closing, we believe that our project illustrates that NLP based sentiment analysis can be combined with a dataset that operates as the ground truth to create a sentiment validity analyzer. This is applicable to fields beyond sports debates, and in an age of disinformation, these AI tools can help identify information by its statistically supported accuracy.



