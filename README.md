# NFL Game Predictor

## Table of Contents

- [Basic Overview](#basic-overview)
  - [Context](#context)
  - [Goal](#goal)
  - [Method](#method)
- [Exploring Data](#exploring-data)
  - [Initial Intake](#initial-intake)
  - [Feature Selection](#feature-selection)
- [Model Selection](#model-selection)
  - [Logistic Regression](#logistic-regression)
  - [Random Forest](#random-forest)
  - [Gradient Boosting](#gradient-boosting)
- [In Action](#in-action)
- [Future Considerations](#future-considerations)

## Basic Overview

### Context

In the words of Danny Ocean from Ocean's 11:

>"The house always wins. Play long enough, you never change the stakes, the house takes you. Unless, when that perfect hand comes along, you bet big, and then you take the house."

For anyone who has played sports gambling in their lives, they know one thing: it is incredibly difficult to beat the house. Even if you pick winners more than 50.1% of the time, you will still lose money in the long run.

### Goal

Develop an NFL game predictor that predicts which team will win the game. The model explores the important features of making the prediction.

Develop betting schemes that can maximize the chances of winning (beat Vegas).

### Method

The intent of this project is to make accurate future predictions. With that in mind, a model will be built using games from previous seasons and then predictions for the latest season, 2019, will be analyzed for determining if this model should be used to beat Vegas.

![Method](images/method.png)

## Exploring Data

### Initial Intake

Data was taken from API provided by https://www.mysportsfeeds.com/. For each team in seasons 2014-2019, approximately 50 stats for each game was stored. The function 'obtain_stats.py' will get the stats from the API. Here is an example of the CSV file that was created:

![Data Intake](images/data_intake.png)

One of the goals of this project is to predict future games. So stats from the current game cannot be used to predict whether or not that team won (i.e., target leakage). 

The function 'nfl_stats_aggregator.py' takes previous games and averages the stats. I started with aggregating the previous six games. When calling the AggregatedStats class, the number of games to aggregate across can be changed.

![Aggregated Stats](images/aggregated_stats.png)

Once the stats were aggregated for each team, the away team and home team had to be merged into one row for a single game. This was done splitting the dataframe based on if the team was playing at home or away, then merging the two dataframes on game_id.

![Merged Dataframe](images/merged_dataframe.png)

### Feature Selection

A heat map was used to find highly correlated stats. For example, as shown below, 'passAvg' and 'passYardPerAtt' were (obviously) very correlated. Based off this, fourteen features were removed.
![Heat Map 1](images/heat_map_1.png)

A goal of this study was to find if I could accurately predict important features using my domain knowledge of the NFL.

For each game, I predicted that the following would be the most important features. As discussed below, I looked at a random forest model and gradient boosted model. A summary of my predicted important features and important features from the models:

| Rank         | My Features               | Random Forest Features    | Gradient Boosted Features   | 
| -------------| -------------             | -------------             |-------------                |
| 1            | Home_Team_Score           | Away_Team_Score           | Away_Team_Score             |
| 2            | Away_Team_Score           | Home_Team_Wins_Past_Games | Home_Team_Wins_Past_Games   |
| 3            | Home_Team_Opponent_Score  | Home_Team_Score           | Home_Team_Score             |
| 4            | Away_Team_Opponent_Score  | Home_Team_Opponent_Score  | Home_Team_Punt_Inside_20_Pct|
| 5            | Home_Team_QB_Rating       | Away_Team_QB_Rating       | Home_Team_Opponent_Score    |
| 6            | Away_Team_QB_Rating       | Home_Team_QB_Rating       | Home_Team_Sacks_Allowed     |
| 7            | Home_Team_Wins_Past_Games | Home_Sacks_Allowed        | Away_Team_Sacks_Allowed     |
| 8            | Away_Team_Wins_Past_Games | Home_Third_Down_Pct       | Away_Team_QB_Rating         |
| 9            | Home_Team_Sacks           | Away_Third_Down_Pct       | Home_Team_Third_Down_Pct    |
| 10           | Away_Team_Sacks           | Away_Sacks_Allowed        | Home_Team_Sack_Yards        |

## Model Selection

### Logistic Regression

This is a classification problem, with my target being if the home team won (1) or lost (0). First, I looked at a logistic regression model but most p-values for the various features were all above 0.05 (most well above that threshold) so I limited the only the statistically signficant features (only five were found to be signficant). The ROC curve is shown below. The accuracy for this model was approximately 65%.

![logistic-reg-roc](images/logistic_regression_roc_curve.png)

### Random Forest

I then looked at a random forest model and using the training data using only the stats that I proposed were important, varied the number of trees and used a 5 K-Fold split to get an average of the accuracy. The accuracy, precision, and recall is shown on the plot below vs the number of trees. For this project, we really only care about accuracy. The accuracy for this set is right around 62% even as the number of trees increase.

![Random-Forest-K-Fold-My-Stats](images/rand_fore_vary_num_trees_my_stats.png)


Then using all of the stats available, the number of trees were varied and used a 5 K-Fold split again to get an average of the accuracy.

![Random-Forest-K-Fold-All-Stats](images/rand_fore_vary_num_trees.png)

As shown, the accuracy doesn't improve by much even by adding in all of the extra features. Also, as shown, good number of trees to choose is 500 for this model.

The full model was built using all of the data from 2014-2018 seasons to develop the important features that the Random Forest found as well as developing an ROC curve to compare against other models.

And finally for the Random Forest model, the ROC curve and AOC score:

![Random-Forest-ROC-AUC](images/rand_fore_roc_curve.png)

### Gradient Boosting

Similar to Random Forest, I used only the stats that I chose as important but varied learning rates for the gradient boosting model with a 5 K-Fold split.

![Gradient-Boosted-K-Fold-My-Stats](images/gradient_boost_vary_learning_rate_my_stats.png)

And for using all stats:

![Gradient-Boosted-K-Fold-All-Stats](images/gradient_boost_vary_learning_rate_all_stats.png)


The ROC curve and AOC curve for gradient boosted:

![Gradient-Boosted-ROC-AUC](images/gradient_boost_roc_curve.png)

## In Action

So what about making some money? Since the logstic model showed the best accuracy and ROC score, that model was chosen to gamble on 2019 NFL games.

As dicussed earlier, the number of games that was averaged across was originally chosen at six. I varied that number to the previous 1 game, 2 games, and all the way up to 6 games.

When a the model makes a prediction, it gives the probability of the home team winning or the away team winning. For example, the model predicts that there is a 70% chance of the home team winning and 30 percent chance of the away team winning.

What if I only want to make a 100 dollar bet if the model is 65 percent sure that it is correct? What about 75 percent sure? As we increase this threshold, the number of games that I bet on will decrease but I have a higher chance (hopefully) of winning money.

![logstic-regression-gambling](images/gains_losses_thresholds_logstic.png)

An interactive chart, using gradient boosting, is best seen here:

https://nbviewer.jupyter.org/github/tylerjwoods/nfl_game_predictor/blob/master/gambling_plotly_nfl.ipynb

## Future Considerations

Using Vegas's prediction of the which team is favored will probably increase the accuracy of the model.

Consider using injuries as a feature.

Scrape games from previous seasons.