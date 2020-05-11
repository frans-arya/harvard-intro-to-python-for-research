import pandas as pd
import numpy as np

from sklearn.model_selection import cross_val_predict
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import r2_score

import matplotlib.pyplot as plt

df = pd.read_csv("moviesdb.csv", index_col=0)

#Create a new column in df called profitable, defined as 1 if the movie revenue (revenue)
#is greater than the movie budget (budget), and 0 otherwise.
#Next, define and store the outcomes we will use for regression and classification. 
#Define regression_target as the string 'revenue'. Define classification_target 
#as the string 'profitable'.

df['profitable'] = df.revenue > df.budget
df['profitable'] = df['profitable'].astype(int)
regression_target = 'revenue'
classification_target = 'profitable'


#Use df.replace() to replace any cells with type np.inf or -np.inf with np.nan.
#Drop all rows with any np.nan values in that row using df.dropna(). Do any further 
#arguments need to be specified in this function to remove rows with any such values?

df = df.replace([np.inf, -np.inf], np.nan)
df = df.dropna(how="any")


#Determine all the genres in the genre column. Make sure to use the strip() function on 
#each genre to remove trailing characters.
#Next, include each listed genre as a new column in the dataframe. Each element of these 
#genre columns should be 1 if the movie belongs to that particular genre, and 0 otherwise. 
#Keep in mind that a movie may belong to several genres at once.

genredf = df.genres
genre = dict()

for items in genredf:
    for item in items.split(', '):
        if item in genre:
            genre[item] += 1
        else:
            genre[item] = 1
            
for key, value in genre.items():
    df[key] = df["genres"].str.contains(key).astype(int)
    

#========================================================

continuous_covariates = ['budget', 'popularity', 'runtime', 'vote_count', 'vote_average']
outcomes_and_continuous_covariates = continuous_covariates + [regression_target, classification_target]
plotting_variables = ['budget', 'popularity', regression_target]

axes = pd.plotting.scatter_matrix(df[plotting_variables], alpha=0.15, \
       color=(0,0,0), hist_kwds={"color":(0,0,0)}, facecolor=(1,0,0))

plt.show()
plt.savefig("linear-regression-movies.pdf")
# determine the skew.
df[outcomes_and_continuous_covariates].skew()

#It appears that the variables budget, popularity, runtime, vote_count, and revenue 
#are all right-skewed. In Exercise 6, we will transform these variables to eliminate 
#this skewness. Specifically, we will use the np.log10() method. Because some of these 
#variable values are exactly 0, we will add a small positive value to each to ensure 
#it is defined; this is necessary because log(0) is negative infinity.
#For each above-mentioned variable in df, transform value x into np.log10(1+x).

for covariate in ['budget', 'popularity', 'runtime', 'vote_count', 'revenue']:
    df[covariate] = df[covariate].apply(lambda x: np.log10(1+x))
    
print(df[outcomes_and_continuous_covariates].skew())

#save df to .csv
df.to_csv("movies_clean.csv")
