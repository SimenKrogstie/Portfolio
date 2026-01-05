import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
from sklearn.impute import SimpleImputer

df_train = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA3/data/train.csv', index_col=[0])
df_test = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA3/data/test.csv', index_col=[0]) 


# From the pairplot we could see there where a lot of outliers that we need to remove
X = df_train.drop('Edible', axis=1)
y = df_train['Edible'] 

# Calculate IQR and determine outliers
Q1 = X.quantile(0.25)
Q3 = X.quantile(0.75)
IQR = Q3 - Q1
outliers = ((X < (Q1 - 4.5 * IQR)) | (X > (Q3 + 4.5 * IQR))).any(axis=1)

# Remove outliers
X_filtered = X[~outliers]
y_filtered = y[~outliers]

X_train, X_test, y_train, y_test = train_test_split(X_filtered, y_filtered, test_size=0.3, random_state=1, stratify=y_filtered) 

impute = SimpleImputer(missing_values=np.nan, strategy='mean')
# Impute train and test data with the feature-mean for respective feature in each dataset.
impute_train = impute.fit(X_train)
X_train = impute_train.transform(X_train)
impute_test = impute.fit(X_test)
X_test = impute_test.transform(X_test)

sc = StandardScaler()
sc.fit(X_train)
X_train_std = sc.transform(X_train)
# Scale the test data
sc.fit(X_test)
X_test_std = sc.transform(X_test)
 
forest = RandomForestClassifier(n_estimators=500, random_state=42)
forest.fit(X_train_std, y_train)

importance = forest.feature_importances_ 
indicies = np.argsort(importance)[::-1]


# Now lets use all the data to train our Random Forrest model for the Kaggle submission, but first we have to preprosses it like we did for the train and test set

# scaaling and fillig in NaN values for the training of the final
sc = StandardScaler()
sc.fit(X_filtered)
X_train_f = sc.transform(X_filtered)

impute_tr = SimpleImputer(missing_values=np.nan, strategy='mean')
impute_tr = impute_tr.fit(X_train_f)
X_train_f = impute_tr.transform(X_train_f)

# I will only use the number of features that gave me the best model
X_train_f = X_train_f[:,list(indicies[:7])] 

# scaling and filling in Nan values for the test set
sc = StandardScaler()
sc.fit(df_test)
X_test_f = sc.transform(df_test)

impute_t = SimpleImputer(missing_values=np.nan, strategy='mean')
impute_t= impute_t.fit(X_test_f)
X_test_f = impute_t.transform(X_test_f)
X_test_f = X_test_f[:,list(indicies[:7])] 

forest = RandomForestClassifier(criterion = 'gini', n_estimators= 100, random_state = 42, bootstrap=True)

forest.fit(X_train_f, y_filtered)

y_test_d = forest.predict(X_test_f)

y_test_dd = pd.DataFrame(y_test_d, columns=["Edible"])
y_test_dd.index.name = "index"
y_test_dd.to_csv("predictions.csv")
