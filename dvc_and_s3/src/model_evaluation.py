import os
import numpy as np
import pandas as pd
import pickle
import json
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
import logging
import yaml
from dvclive import Live

"""
This calculates the report card for our final trained model using hiddent test data.
It forces a model to see msgs which never seen before X_test, makes it guess whether they spam or ham then compares those guesses with real ans to compute 4 critical evaluation scores.
"""

# Logging
logs_dir = './dvc_and_s3/logs'
os.makedirs(logs_dir, exist_ok=True)

# logging config
logger = logging.getLogger('model_evaluation')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(logs_dir, 'model_evaluation.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_params(params_path: str) -> dict:
    """Load parameters from a YAML file"""
    try:
        with open(params_path, 'r') as file:
            params = yaml.safe_load(file)
        logger.debug('Parameters retrieved from %s', params_path)
        return params
    except FileNotFoundError:
        logger.error('File not found: %s', params_path)
        raise
    except yaml.YAMLError as e:
        logger.error('YAML error: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error: %s', e)
        raise

def load_model(file_path:str):
    """Load the trained model from a file"""
    try:
        with open(file_path, 'rb') as file:     # rb = read binary
            model = pickle.load(file)
        logger.debug('Model loaded from %s', file_path)
        return model
    except FileNotFoundError:
        logger.error('File not found: %s', file_path)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the model: %s', e)
        raise

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from CSV file"""
    try:
        df = pd.read_csv(file_path)
        logger.debug('Data loaded from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the CSV file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise

def evaluate_model(clf, X_test:np.ndarray, y_test:np.ndarray) -> dict:
    """Evaluate the model and return the evaluation metrics"""
    try:
        # model evaluates test data & outputs a direct, final guess for each row: 0(ham) or 1(spam)
        y_pred = clf.predict(X_test)
        # this tells us the probability 
        y_pred_proba = clf.predict_proba(X_test)[:, 1]

        accuracy = accuracy_score(y_test, y_pred)   # overall % of correct guesses total correct/total msgs
        precision = precision_score(y_test, y_pred)     # how many of this were spam?
        #In a spam filter, you want high precision. If your precision is low, it means your model is aggressively blocking normal, important emails (like job offers or bank alerts) and misclassifying them as spam.
        recall = recall_score(y_test, y_pred)   # Out of all the actual spam messages hidden in the dataset, how many did the model successfully catch?
        #  If your recall is low, your spam filter is too weak, and a lot of annoying junk mail is slipping right through into the user's main inbox.
        auc = roc_auc_score(y_test, y_pred_proba)   # Area Under the ROC Curve
        # This evaluates how good the model is at separating the probabilities of the two classes. A score of 1.0 means perfect separation; a score of 0.5 means the model is just guessing completely at random.

        metrics_dict = {
            'accuracy':accuracy,
            'precision':precision,
            'recall':recall,
            'auc':auc
        }
        logger.debug('Model evaluation metrics calculated')
        return metrics_dict
    except Exception as e:
        logger.error('Error during model evaluation: %s', e)
        raise

def save_metrics(metrics:dict, file_path:str) -> None:
    """Save evaluation metrics to json file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        with open(file_path, 'w') as file:
            json.dump(metrics, file, indent=4)
        logger.debug('Metrics saved to %s', file_path)
    except Exception as e:
        logger.error('Error occurred while saving the metrics: %s', e)
        raise

def main():
    try:
        params = load_params(params_path='C:/Projects/MLops/dvc_and_s3/params.yaml') 
        clf = load_model('./models/model.pkl')
        test_data = load_data('./dvc_and_s3/data/processed/test_tfidf.csv')

        X_test = test_data.iloc[:, :-1].values      # this is 50 features
        y_test = test_data.iloc[:, -1].values       # labels 0 or 1

        metrics = evaluate_model(clf, X_test, y_test)

        # experiment tracking using dcvlive
        with Live(save_dvc_exp=True) as live:
            live.log_metric('accuracy', accuracy_score(y_test, y_test))
            live.log_metric('precision', precision_score(y_test, y_test))
            live.log_metric('recall', recall_score(y_test, y_test))
            live.log_params(params)

        save_metrics(metrics, 'reports/metrics.json')

    except Exception as e:
        logger.error('Failed to complete ,the model evaluation process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()