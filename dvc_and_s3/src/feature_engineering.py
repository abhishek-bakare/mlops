"""
What is feature engineering: is the process of transforming raw, messy test data into clean, structural numerical variables(features) that a mathematical model can actaully compute and learn.
In your specific project—which is a Spam Classifier—the machine learning algorithms cannot read sentences, understand English grammar, or interpret context. They can only calculate probabilities, matrices, and vectors. 
Feature engineering bridges this gap by converting text fingerprints into structured numerical inputs.

In text classification, occurs in 2 phases: Text preprocessing & vectorization
Text preprocessing which we already done like tokenization, stopwrods, lowercasing, stemming, etc.

Vectorization (converting words to math): 2 types bag of words and tfidf vectorizer
Bang of words: It creates a massive spreadsheet where every unique word in your entire dataset gets its own column. For each text message, it simply counts how many times that word appears.

Vectorizer: Short for Term Frequency-Inverse Document Frequency.
This is a smarter technique. It doesn't just count words; it calculates a score. If a word appears a lot in one specific message (like "prize"), but is rare in the rest of the dataset, it gets a high score. If a word is common everywhere, it gets a low score.

"""

import pandas as pd
import os, yaml, logging
from sklearn.feature_extraction.text import TfidfVectorizer

# Ensure logs directory exist
logs_dir = './dvc_and_s3/logs'
os.makedirs(logs_dir, exist_ok=True)

# logging configuration
logger = logging.getLogger('feature_engineering')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(logs_dir, 'feature_engineering.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def load_params(params_path:str) -> dict:
    """Load parameters from YAML file"""
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

def load_data(file_path: str) -> pd.DataFrame:
    """Load data from a csv file"""
    try:
        df = pd.read_csv(file_path)
        df.fillna('', inplace=True)     # finds all missing or blank values(NaN) in dataframe & replaces with empty text string ""
        logger.debug('Data loaded and NaNs filled from %s', file_path)
        return df
    except pd.errors.ParserError as e:
        logger.error('Failed to parse the csv file: %s', e)
        raise
    except Exception as e:
        logger.error('Unexpected error occurred while loading the data: %s', e)
        raise


def apply_tfidf(train_data: pd.DataFrame, test_data:pd.DataFrame, max_features:int) -> tuple:
    """Apply Tfidf to the data"""
    try:
        # vectorizer func and vocabulary size limiter means if dataset has 10000 unique words setting max--=3000 tells to keep only top 3000 most imp words and drop rest.
        # This prevents your dataset from getting too massive
        vectorizer = TfidfVectorizer(max_features=max_features)

        X_train = train_data['text'].values     # values will convert pandas column into raw numpy arrays for faster processing
        y_train = train_data['target'].values
        X_test = test_data['text'].values
        y_test = test_data['target'].values

        X_train_bow = vectorizer.fit_transform(X_train)     # fit()-reads all training msgsto learn the vocabulary and pick the top max_features words transform()- converts into tfidf scores
        X_test_bow = vectorizer.transform(X_test)     # here we only trnsform

        train_df = pd.DataFrame(X_train_bow.toarray())  # COnverts mathematical matrix into structural pandas df. 
        train_df['label'] = y_train
        print(train_df['label'])

        test_df = pd.DataFrame(X_test_bow.toarray())
        test_df['label'] = y_test

        logger.debug('tfidf applied and data transformed')
        return train_df, test_df
    except Exception as e:
        logger.error('Error during bag of words transformation: %s', e)
        raise

def save_data(df:pd.DataFrame, file_path: str) -> None:
    """Save the dataframe to a CSV file"""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        df.to_csv(file_path, index=False)
        logger.debug('Data saved to %s', file_path)
    except Exception as e:
        logger.error('Unexpected error occurred while saving the data: %s', e)
        raise

def main():
    try:
        params = load_params(params_path='C:/Projects/MLops/dvc_and_s3/params.yaml')
        max_features = params['feature_engineering']['max_features']
        # max_features = 50

        train_data = load_data('./dvc_and_s3/data/interim/train_processed.csv')
        test_data = load_data('./dvc_and_s3/data/interim/test_processed.csv')

        train_df, test_df = apply_tfidf(train_data, test_data, max_features)

        save_data(train_df, os.path.join("./dvc_and_s3/data", "processed","train_tfidf.csv"))
        save_data(test_df, os.path.join("./dvc_and_s3/data", "processed","test_tfidf.csv"))
    except Exception as e:
        logger.error('Failed to complete the feature engineering process: %s', e)
        print(f"Error: {e}")

if __name__ == '__main__':
    main()