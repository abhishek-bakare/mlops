import mlflow           # manage the machine learning lifecycle, handle experiments, log parameters, and store artifacts
import mlflow.sklearn
from sklearn.datasets import load_wine      # built-in classic toy dataset containing chemical analysis features of 3 different Italian wines
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split        # helper utility that randomly splits your data into a training set and a testing set
from sklearn.metrics import accuracy_score, confusion_matrix        # evaluation matrics
import matplotlib.pyplot as plt
import seaborn as sns       # statistical data visualization library built on top of Matplotlib

mlflow.set_tracking_uri("http://127.0.0.1:5000")        # setting up tracking data where to send

#load wine dataset
wine = load_wine()          # Loads dataset into memory
X = wine.data               # Extracts the input features (the chemical properties like alcohol content, magnesium, color intensity).
y = wine.target             # Extracts the ground-truth target output labels (the 3 distinct wine cultivars, represented as 0, 1, or 2)

# train test split
# Splits the dataset into training data (90%) and evaluation data (10%)
# random_state=42 acts as a pseudo-random seed to guarantee that the split is identical every single time you execute this script
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10, random_state=42)

# define the params for RF model
max_depth = 10      # max_depth limits how deep each decision tree can grow
n_estimators = 5        # n_estimators dictates that the forest will combine the outputs of exactly 5 decision trees

# mention your experiment below
# Groups our all runs under this folder inside UI but in code folder name is random alphanums
mlflow.set_experiment('Sample-1')   

with mlflow.start_run():        # starts an active loggin block
    rf = RandomForestClassifier(max_depth=max_depth, n_estimators=n_estimators, random_state=42)
    rf.fit(X_train, y_train)    # Trains the model by letting it uncover patterns connecting the chemical properties (X_train) to their known wine classes (y_train)

    y_pred = rf.predict(X_test)         # Passes the held-out validation features (X_test) into the trained model to generate fresh predictions
    accuracy = accuracy_score(y_test, y_pred)   # Compares those fresh model predictions (y_pred) against the real answer key (y_test) to compute your final score

    # Logging Metadata & Visual Charts
    mlflow.log_metric('accuracy', accuracy)     # saves dynamic performance
    mlflow.log_param('max_depth', max_depth)    # 
    mlflow.log_param('n_estimators', n_estimators)

    # creating a confusion matrix plot
    # A confusion matrix plot is a visual chart that shows exactly how well a machine learning classification model is performing.
    cm = confusion_matrix(y_test, y_pred)
    plt.figure(figsize=(6,6))
    sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=wine.target_names, yticklabels=wine.target_names)    # color coding
    plt.ylabel('Actual')
    plt.xlabel('Predicted')
    plt.title('Confusion Matrix')

    # save plot
    plt.savefig("confusion-matrix.png")

    #log artifacts using mlflow
    mlflow.log_artifact("confusion-matrix.png")     # upload image to mlflow server 
    mlflow.log_artifact(__file__)           # exact file1.py copy will be uploaded to mlfow

    # tags
    mlflow.set_tags({"Author": 'Abhishek',"Project":'Wine classification'})

    # log the model
    mlflow.sklearn.log_model(sk_model=rf, 
                            artifact_path="Random-Forest-Model", 
                            skops_trusted_types=["sklearn.tree._tree.Tree"])

    print(accuracy)
