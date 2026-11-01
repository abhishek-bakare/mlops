from sklearn.model_selection import GridSearchCV    #"Grid Search Cross-Validation" tool. It systematically works through a predefined grid of combinations of hyperparameters and determines which combination yields the best model performance
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split    # helper utility that randomly splits your data into a training set and a testing set
from sklearn.datasets import load_breast_cancer     # sample dataset
import pandas as pd
import mlflow       # manage the machine learning lifecycle, handle experiments, log parameters, and store artifacts

# Load breast cancer dataset
data = load_breast_cancer()
X = pd.DataFrame(data.data, columns=data.feature_names)     # X contains the physical metrics of the tumors (like radius, texture, perimeter)
y = pd.Series(data.target, name='target')       # y contains the true target classification (0 for malignant, 1 for benign)

# Splitting into training and testing sets
# X (Features / Inputs): This is a 2D matrix (DataFrame) containing all the clues or measurements the model will use to learn. 
# In our breast cancer dataset, X contains 30 columns of physical properties like mean radius, mean texture, and mean perimeter. 
# The model reads these inputs to guess the outcome

# y (Target / Output / Label): This is a 1D column (Series) containing the actual answers or categories you want the model to predict. 
# For this dataset, y holds a list of 0s (malignant tumor) and 1s (benign tumor).
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# creating the RandomForestClassifier model
rf = RandomForestClassifier(random_state=42)

#Defining the parameter grid for GridSearchCV
# 3 options for no of trees, 4 options for how deep they can grow. means 3 * 4 = 12 variations to check
param_grid = {
    'n_estimators': [10, 50, 100],
    'max_depth': [None, 10, 20, 30]
}

# applying GridSearchCV
# cv=5 means 5-fold cross-validation (the training data is split into 5 subsets; the model trains on 4 and tests on 1, repeating this 5 times for every single combination)
# This results in 12 variations × 5 folds = 60 total model runs
# n_jobs=-1 tells your computer to use all available processor cores to run these combinations in parallel
# verbose=2 forces the console to print out progress logs while running
grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=5, n_jobs=-1, verbose=2)

# # Run without mlflow from here
# grid_search.fit(X_train, y_train)

# # Displaying the best params and best score
# best_params = grid_search.best_params_
# best_score = grid_search.best_score_

# print(best_params)
# print(best_score)
# # Till here

mlflow.set_experiment('Breast-cancer-rf-hp')

with mlflow.start_run() as parent:
    grid_search.fit(X_train, y_train)       # Executes the actual mathematical process of training and testing those 60 iterations across your computer cores

    # log all the child runs
    # Loops through the 12 distinct hyperparameter variations evaluated during the grid search
    # nested=True: Creates an organized hierarchy. Instead of cluttering your MLflow dashboard with 12 separate unlinked rows, it nests these Child Runs inside the primary Parent Run
    # understand this for loop in projectflow
    for i in range(len(grid_search.cv_results_['params'])):
        with mlflow.start_run(nested=True) as child:
            mlflow.log_params(grid_search.cv_results_["params"][i])
            mlflow.log_metric("accuracy", grid_search.cv_results_["mean_test_score"][i])

    # displaying bets parameters and best score
    # Extracts the single winning setting and score from the completed matrix and saves them onto the primary Parent Run overview sheet
    best_params = grid_search.best_params_
    best_score = grid_search.best_score_

    # log params, metric
    mlflow.log_params(best_params)
    mlflow.log_metric("accuracy", best_score)

    # log training data
    # Creates a copy of your training features and target labels together
    train_df = X_train.copy()
    train_df['target'] = y_train

    train_df = mlflow.data.from_pandas(train_df)    # transform it to mlflow datsets and logs it to ui
    mlflow.log_input(train_df, "training")

    # log the test data
    test_df = X_test.copy()
    test_df['target'] = y_test

    test_df = mlflow.data.from_pandas(test_df)
    mlflow.log_input(test_df, "testing")

    # log source code
    mlflow.log_artifact(__file__)

    # log best model
    #mlflow.sklearn.log_model(grid_search.best_estimator_, "random_forest")
    # log the model
    mlflow.sklearn.log_model(sk_model=grid_search.best_estimator_, 
                                artifact_path="Random-Forest-Model", 
                                registered_model_name="Breast-Cancer-RF-Model",     # to register a model
                                skops_trusted_types=["sklearn.tree._tree.Tree"])

    # set tags
    mlflow.set_tags({"Author": 'Abhishek',"Project":'Breast cancer'})

    print(best_params)
    print(best_score)
