import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import numpy as np

from sklearn.model_selection import train_test_split, KFold, GridSearchCV, cross_val_predict
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.decomposition import PCA
from sklearn.metrics import mean_absolute_error, accuracy_score

from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor

# Reading the train and test data
df_train = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA5/data/train.csv')
df_test = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA5/data/test.csv')

# Removing 'Average Temperature During Storage (celsius)' from train_df
train_df = df_train.drop('Average Temperature During Storage (celcius)', axis=1)



# Defining features and target.
X = train_df.drop('Scoville Heat Units (SHU)', axis=1)
y = train_df['Scoville Heat Units (SHU)']



# Split data in train and test.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

num_cols = X_train.select_dtypes(include=['float64']).columns.to_list()
cat_cols = X_train.select_dtypes(include=['object']).columns.to_list()



# Pipeline to preprocesses the numerical data
num_trans = Pipeline(
    ('imputer', SimpleImputer(strategy='mean')),
    ('scaler', StandardScaler())
)

# Pipeline to preprocess the categorical data
cat_trans = Pipeline(
    ('imputer', SimpleImputer(strategy='most_frequent')),
    ('onehot', OneHotEncoder(handle_unknown='ignore'))
)

# Preprocessor that scale numerical data, encode categorical data
# and imputes both datatypes.
preprocessor = ColumnTransformer(
    transformers=[
        ('num', num_trans, num_cols),
        ('cat', cat_trans, cat_cols)
    ])





# Create a pipeline for the classification model
clf_pipeline = Pipeline([
    ('preprocesor', preprocessor),
    ('scaler', StandardScaler()),
    ('rf', RandomForestClassifier())
])

# Parameter grid for the classifier
clf_param_grid = {
    'rf__n_estimators': [100, 200, 300],
    'rf__max_depth': [None, 10, 20, 30],
    'rf__min_samples_split': [2, 5, 10],
    'rf__min_samples_leaf': [1, 2, 4]
}

# Splitting dataset to 5 folds for the gridsearch.
cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Grid search over 5-fold cross validation defined by cv.
clf_gridsearch = GridSearchCV(clf_pipeline, clf_param_grid, cv=cv, scoring='neg_mean_absolute_error', verbose=1)

# Fitting gridsearch to trainig data. 
clf_gridsearch.fit(X_train, (y_train > 0).astype(int))


# Printing out best parametersthe grid search.
y_pred_class = clf_gridsearch.predict(X_test)
print('Best parameters: ', clf_gridsearch.best_params_)


# Identifying the spicy peppers
spicy_peppers = y_train > 0
X_train_spicy, y_train_spicy = X_train[spicy_peppers], y_train[spicy_peppers]
X_test_spicy, y_test_spicy = X_test[y_test > 0], y_test[y_test > 0]

# Pipeline for the regression
reg_pipeline = Pipeline([
    ('preprocessor', preprocessor),
    ('reg', RandomForestRegressor(n_estimators=100, random_state=42))
])

# The parameter grid for the regression model
reg_param_grid= {
    'reg__n_estimators' : [100, 200, 300],
    'reg__max_depth' : [None, 10, 20, 30],
    'reg__min_samples_split' : [2, 5, 10],
    'reg__min_samples_leaf' : [1, 2, 4]
}

# Splitting dataset to 5 folds for the gridsearch.
cv = KFold(n_splits=5, shuffle=True, random_state=42)

# Grid search over 5-fold cross validation defined by cv.
reg_gridsearch = GridSearchCV(reg_pipeline, reg_param_grid, cv=cv, scoring='neg_mean_absolute_error', verbose=1)

# Fitting the gridsearch to training data
reg_gridsearch.fit(X_train_spicy, y_train_spicy)

# Printing out the best parameters from the grid search.
print('Best parameters: ', reg_gridsearch.best_params_)

# Evaluating the best classifier
best_clf = clf_gridsearch.best_estimator_
y_pred_clf = best_clf.predict(X_test)
accuracy = accuracy_score(y_test > 0, y_pred_clf)
print(f"Classification accuracy: {accuracy:.2f}")

# Evaluating the best regressor
best_reg = reg_gridsearch.best_estimator_
y_pred_reg = best_reg.predict(X_test_spicy)
mae = mean_absolute_error(y_test_spicy, y_pred_reg)
print(f"Mean absolute error: {mae:.2f}")
