Using logistic regression and random forest to predict the Ballon d'Or winner. Ballon d'Or is the best footballer of the year award given every year (except 2020 due to the pandemic) in football. The project aims to train the model with past years and predict this year's winner. 

Obtaining statistics: 

“stats.py” contains the statistics. “functions.py” contains the necessary functions. 

In this github repository https://github.com/probberechts/soccerdata there is a pre-designed web scraper. Using it I get the statistics from the website FBref. Besides “Standard” the following 8 types of statistics are obtained.

![Categories](https://github.com/nebulut/ballondor_prediction/blob/main/categories.png)

3 main leagues were looked at for statistics. These are: Champions League (UCL), Local Leagues (LG) and World Cup (WC). The World Cup is organized every 4 years and therefore the columns for the years without a World Cup were added manually and all were made “0”. 

I first thought to look at the top 100 players with the highest market value because it is too much data load to analyze all the players, but then I realized that in some seasons (for example: 21-22) a player without a market value in the top 100 was voted the best player. Then I thought to look at the 200 players with the most minutes in the UCL, the Champions League, and every year I looked at this, there were no exceptions and one player from the top 200 won the Ballon d'Or. So I sifted the data a bit more and reduced the processing load. 

There are 513 statistics for each player in 3 leagues. 

The seasons that are eliminated and corrected in the “stats.py” file are saved in the file named “seasons”. You may want to save the season you want to predict in the folder named “to_predict” where we use the season and test the model. 

Normalization: 

For normalization, each season is normalized separately. Min-max normalization was used for this process. All seasons in the “seasons” folder are normalized by running the “”normalize.py file. The normalized seasons are saved in the folder named “normalized_seasons”. 

Model Training: 

Two different models were used: Logistic Regression and Random Forest. The dataframes of the normalized seasons are combined before training and the model is trained. 

Model Testing: 

Models were tested for each season. While testing each season, care was taken not to use it in model training. For example, when testing the “08-09” season, the “08-09” season was not used in the training. For example, the results for the two seasons are saved in the folder named “results” as follows:

![Random Forest Results 23-24](https://github.com/nebulut/ballondor_prediction/blob/main/rf.png) ![Logistic Regression Results 23-24](https://github.com/nebulut/ballondor_prediction/blob/main/lr.png)

The first image gives the results for random forest and the second image for logistic regression. These estimates are for 23-24, this year's season. 

The test results for all seasons were as follows: 

![All Results](https://github.com/nebulut/ballondor_prediction/blob/main/all_results.png)

In the seasons written in red, the models guessed wrong. For this season, both models predicted “Kylian Mbappe”. As this season is not yet over, we don't know if they are correct. Although the model successes are similar, Random Forest predicted one more season wrong.

Steps to make predictions:
1. Get the stats by entering the desired years at the top of the stats.py file.
2. Add the target season to the folder named to_predict.
3. Normalize all seasons by running the file named normalize.py.
4. To train the model with the normalized seasons, run the train.py file of the desired model and train the model with the normalized seasons.
5. Enter the season you want to test in the model's test.py file and get the results.

Limitations:
The stats are usually only numerical and offensive oriented, which can lead to some shortcomings. For example, the winner of the “05-06” season was a defender but the model predicts an attacker. The model could be improved with more data. It could also focus on leagues such as Euro Cup and Copa America. The weights of the leagues can be adjusted.

