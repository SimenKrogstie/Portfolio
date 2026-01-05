import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from numpy import interp

from sklearn.model_selection import train_test_split, cross_val_predict, GridSearchCV, StratifiedKFold
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.decomposition import PCA
from sklearn.discriminant_analysis import LinearDiscriminantAnalysis as LDA
from sklearn.metrics import f1_score, ConfusionMatrixDisplay, roc_curve, auc
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

C = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0, 1000.0]
n_components = [1, 2, 3, 4, 5, 6]
gamma = [0.0001, 0.001, 0.01, 0.1, 1.0, 10.0, 100.0] 

df_train = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA4 second/data/train.csv')
df_test = pd.read_csv('/Users/simenkrogstie/Documents/Programming/DAT200/Compulsary Assignments/CA4 second/data/test.csv')

# Defining the features and targets
X = df_train.drop('Diagnosis', axis=1)
y = df_train['Diagnosis']

# Splitting data in train and test.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)

# Sorting between numerical and categorical columns.
cat_cols = ['Alcohol_Use (yes/no)', 'Diabetes (yes/no)', 'Gender', 'Obesity (yes/no)']
num_cols = X_train.columns.drop(cat_cols).to_list()

# Only scaling the numerical data.
preprocessor = ColumnTransformer([
    ('num', StandardScaler(), num_cols),
    ('cat', 'passthrough', cat_cols)
    ])

lda_pipeline = Pipeline([('scaler', preprocessor),
                         ('LDA', LDA())])

lr_ldapipeline = Pipeline([
    ('lda pipeline', lda_pipeline),
    ('lr', LogisticRegression(penalty='l2', random_state=42))
])

lda_y_hat_lr = cross_val_predict(lr_ldapipeline, X_train, y_train, cv=10)
f1_lda_lr = f1_score(y_train, lda_y_hat_lr, average='macro')
print(f'Logistic Regression with LDA gives F1-score: {round(f1_lda_lr * 100, 2)}')


# Hyperparametertuning of the best performing logistic regression pipeline. 

# A logistic Regression pipeline with no 
logreg_pipeline = Pipeline([
    ('lda', lda_pipeline),
    ('logreg', LogisticRegression())
])

# The parameter grid for the logistic regression pipeline. Made to a list of dictionaries.
# This is to ensure the grid search find the best possible combination of hyperparameters.
logreg_param_grid = [
    {'lda__LDA__n_components' : n_components, 'logreg__penalty' : ['l1'], 'logreg__solver' : ['liblinear'], 'logreg__C' : C},
    {'lda__LDA__n_components' : n_components, 'logreg__penalty' : ['l2'], 'logreg__solver' : ['liblinear', 'newton-cg'], 'logreg__C' : C}
    ]

# Splitting the dataset into 5-folds for the grid search.
cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

# Grid search over a 5-fold cross-validation defined by cv.
logreg_gridsearch = GridSearchCV(estimator=logreg_pipeline, param_grid=logreg_param_grid, scoring='f1_macro', cv=cv, verbose=1)

# Fit the grid search to the training data.
logreg_gridsearch.fit(X_train, y_train)

# Printing out the best parameters and the respective f1-score.
print('Best parameters: ', logreg_gridsearch.best_params_)
print('Best score: ', logreg_gridsearch.best_score_)

# Evaluation of the logistic regression model after tuning the hyperpareters.
best_logreg = logreg_gridsearch.best_estimator_
y_pred_logreg = best_logreg.predict(X_test)
f1_logreg = f1_score(y_test, y_pred_logreg, average='macro')
print(f'F1-score logreg after tuning hyperparameters: {f1_logreg}')

# Sorting out the columns in the test data with categorical data.
cat_cols_test = df_test.select_dtypes(include=['object']).columns

# for-loop that loops through cols in cat_cols_test and encode the categorcal data to zeros and ones. 
for i in cat_cols_test:
    class_mapping = {label: i for i, label in enumerate(np.unique(df_test[i]))}
    df_test[i] = df_test[i].map(class_mapping)

# Fit the model I am using for the Kaggle submission on the whole training dataset. 
best_logreg.fit(X, y) 

# Prediction on the test dataset. 
y_pred = best_logreg.predict(df_test)

# Creating Kaggle subbmission .csv file.
y_final = pd.DataFrame(y_pred, columns=["Diagnosis"])
y_final.index.name = "index"
y_final.to_csv("predictions3.csv")