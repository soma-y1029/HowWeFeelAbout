# HowWeFeelAbout
### Deploy
https://howwefeelabout.herokuapp.com/

## Introduction
HOW WE FEEL ABOUT is a web-based app that analyzes Twitter user's sentiment based on the provided query. The text classification model is built with labeled 10K sample tweets provided by NLTK. It receives a keyword from a user and classifies tweets based on the model. The tweets to be classified are obtained from twitter.com of most recent 200 tweets based on the keyword. This sentiment analyzer is to understand our emotions on a certain topic. Django web framework is used for effective communication between frontend and backend. Heroku is used to deploy our project. Frontend is developed by Solbi You. Backend is developed by Soma Yoshida.

![](https://i.imgur.com/4rlPr4w.png)

## Use Cases
Sentimental analysis is used by various industries to analyze customers’ sentiment on a certain topic. It is mainly used to improve a customer experience by tracking customer sentiment and how it changes over time. For our project, we allow the user to enter the keyword and print out how people in general feel about that certain topic on the scale of 0 to 100. We thought it could be helpful to choose what we should work on for our future projects as well as our future business if we ever start one. 
1. Enter a query that you want to perform sentiment analysis for. 
2. Hit Enter key or submit button to receive returned sentiment value from 0 to 100.


### Sample output

Example of 'good'.
![](https://i.imgur.com/nn8eEU8.png)

Example of 'bad'
![](https://i.imgur.com/epSMpvo.png)


## Components
Django web framework is used for effective communication between frontend and backend. Heroku is used to deploy our project.

### Front-end
In django, there are built-in template tags and filters, which allow the programmer to use if statements in the html. If statements were used to show different icons based on the result.  I created a progress bar to display the result that shows the positiveness of a certain keyword. On each end of the progress bar, happy and angry emojis are placed to effectively demonstrate the positiveness of the keyword. Most of the icons for this project came from Font awesome, which is one of the top open source projects on GitHub. Various fonts, used in this application, are from Google fonts.  I used javascript to make the progress bar more dynamic and to enable the accordion feature for the Q&A.


### Back-end
<p>The technologies used in this project are: Tweepy for obtaining real tweets based on a given query, NLTK for labeled sample tweets, Spacy and Scikit Learn for processing sentiment analysis. Multinomial Naive Bayes is used to train the text classification model. Pickle is applied to data (mainly the model). </p>
<p>The backend application can generate a text classification model for sentiment analysis, process sentiment analysis algorithm with 200 actual tweets obtained from twitter.com based on the given query, and return the sentiment in a number of positiveness with some sample tweets of the positive and negative and total number of tweets actually obtained from twitter.com. </p>
<p>Pickle is utilized to store data and read stored data from files. It allows the program to retrieve the pre-built text classification model so that the algorithm can invoke the existing model every time the user opens the app. This is very crucial for this project as it avoids building the same model every time the algorithm runs as it takes a couple of minutes to just build the model with 10K sample tweets. </p>

## Implementation
### Test cases
To test the text classification model, we have used a module of scikit learn. It allows us to see the accuracy of the built model by splitting prelabeled 10K sample tweets to 70%, 30% for  training and testing respectively. The accuracy score is returned by number and the accuracy was 71% with Multinomial Naive Bayes.
