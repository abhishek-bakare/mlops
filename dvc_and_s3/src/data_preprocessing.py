import os, logging
import pandas as pd
from sklearn.preprocessing import LabelEncoder
from nltk.stem.porter import PorterStemmer
from nltk.corpus import stopwords
import string, nltk

nltk.download('stopwords')
nltk.download('punkt')

# ensuring logs dir exists
logs_dir = './dvc_and_s3/logs'
os.makedirs(logs_dir, exist_ok=True)

# Setting up logger
logger = logging.getLogger('data_preprocessing')
logger.setLevel('DEBUG')

console_handler = logging.StreamHandler()
console_handler.setLevel('DEBUG')

log_file_path = os.path.join(logs_dir, 'data_preprocessing.log')
file_handler = logging.FileHandler(log_file_path)
file_handler.setLevel('DEBUG')

formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
console_handler.setFormatter(formatter)
file_handler.setFormatter(formatter)

logger.addHandler(console_handler)
logger.addHandler(file_handler)

def transform_text(text):
    """
    Transforms the input text by converting it to lowercase, tokenizing, removing stopwords and punctuation, and stemming.
    """
    ps = PorterStemmer()
    text = text.lower()
    # Tokenize means breaking down continous string text into smaller, individual units called tokens. ex: ['WINNER', '!', '!', 'As', 'a', 'valued', 'network', 'customer', 'you', 'have', 'been', 'selected']
    # we cannot analyze string in a sentence string, it can allows filters like we used below, computers cant understand sentences.
    text = nltk.word_tokenize(text)     # tokenize the text
    text = [word for word in text if word.isalnum()]        # remove non-alphanumeric tokens
    text = [word for word in text if word not in stopwords.words('english') and word not in string.punctuation]     # remove stopwords and punctuations
    text = [ps.stem(word) for word in text]     # stem the words means running, runs, ran holds the same meanning run so instead of forcing model to learn all three words stemming collapses into 1. 
    return " ".join(text)   # joins the tokens back into single string

def preprocess_df(df, text_column='text', target_column='target'):
    """
    Preprocesses the DataFrame by encoding the target column, removing duplicates, and transforming the text column.
    """
    try:
        logger.debug('Starting preprocessing for DataFrame')
        # encode the target column
        # LabelEncoder is scikit tool utility used to convert text based labels into distinct numerical values
        # Why we use this? ML algorthm cannot understand raw text and its purely mathematical model, labelencoder assigns unique digits to each unique text labels
        encoder = LabelEncoder()
        df[target_column] = encoder.fit_transform(df[target_column])
        print(df[target_column])
        logger.debug('Target column encoded')

        # remove duplicates row
        df = df.drop_duplicates(keep='first')
        logger.debug('Duplicates removed')

        # apply text transformations to specified text column, in Pandas this is fast way to select rows, col and apply.
        # df.loc[rows (: all rows), columns] = apply is loop shortcut in pandas instead of using slow for loop
        df.loc[:, text_column] = df[text_column].apply(transform_text)
        print(df.loc[:, text_column])
        logger.debug('Text column transformed')
        return df
    except KeyError as e:
        logger.error('Column not found %s', e)
        raise
    except Exception as e:
        logger.error('Error during text normalization: %s', e)
        raise

def main(text_column='text', target_column='target'):
    """
    Main function to load raw data, preprocess it, and save the processed data.
    """
    try:
        # fetch the data from ./dvc_and_s3/data/raw
        train_data = pd.read_csv('C:/Projects/MLops/dvc_and_s3/data/raw/train.csv')
        test_data = pd.read_csv('C:/Projects/MLops/dvc_and_s3/data/raw/test.csv')
        logger.debug('Data loaded properly')

        # transform the data
        train_processed_data = preprocess_df(train_data, text_column, target_column)
        test_processed_data = preprocess_df(test_data, text_column, target_column)

        # store the data 
        data_path = os.path.join("./dvc_and_s3/data", "interim")
        os.makedirs(data_path, exist_ok=True)

        train_processed_data.to_csv(os.path.join(data_path, "train_processed.csv"), index=False)
        test_processed_data.to_csv(os.path.join(data_path, "test_processed.csv"), index=False)
        logger.debug('Processed data saved to %s', data_path)

    except FileNotFoundError as e:
        logger.error('File not found: %s', e)
    except pd.errors.EmptyDataError as e:
        logger.error('No data: %s', e)
    except Exception as e:
        logger.error('Failed to complete the data transformation process: %s', e)
        print(f"Error: {e}")

if __name__=='__main__':
    main()