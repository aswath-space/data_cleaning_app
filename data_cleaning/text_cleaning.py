import nltk
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import PorterStemmer, WordNetLemmatizer
from nltk.corpus import stopwords
import re
import string
import spacy
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from sklearn.feature_extraction.text import TfidfVectorizer

# Download necessary NLTK data
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('stopwords')
nltk.download('vader_lexicon')

# Load spaCy model
nlp = spacy.load('en_core_web_sm')

def tokenize_text_nltk(df, column):
    """
    Tokenize text using NLTK's word_tokenize.
    This method splits the text into individual words.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of tokenized words.
    """
    df[f'{column}_tokens'] = df[column].apply(word_tokenize)
    return df

def tokenize_text_sklearn(df, column):
    """
    Tokenize text using scikit-learn's CountVectorizer.
    This method converts text into a matrix of token counts.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    scipy.sparse.csr.csr_matrix, np.ndarray: Token count matrix and feature names.
    """
    vectorizer = CountVectorizer()
    tokens = vectorizer.fit_transform(df[column])
    return tokens, vectorizer.get_feature_names_out()

def stem_text(df, column):
    """
    Stem text using NLTK's PorterStemmer.
    This method reduces words to their root form.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of stemmed text.
    """
    stemmer = PorterStemmer()
    df[f'{column}_stemmed'] = df[column].apply(lambda x: ' '.join([stemmer.stem(word) for word in x.split()]))
    return df

def lemmatize_text(df, column):
    """
    Lemmatize text using NLTK's WordNetLemmatizer.
    This method reduces words to their base form, considering the context.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of lemmatized text.
    """
    lemmatizer = WordNetLemmatizer()
    df[f'{column}_lemmatized'] = df[column].apply(lambda x: ' '.join([lemmatizer.lemmatize(word) for word in x.split()]))
    return df

def remove_stopwords(df, column):
    """
    Remove stopwords from text.
    Stopwords are common words that do not carry significant meaning (e.g., "and", "the").

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of text without stopwords.
    """
    stop_words = set(stopwords.words('english'))
    df[f'{column}_no_stopwords'] = df[column].apply(lambda x: ' '.join([word for word in x.split() if word.lower() not in stop_words]))
    return df

def normalize_text(df, column):
    """
    Normalize text by converting to lowercase, removing punctuation and digits.
    This method standardizes the text format.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of normalized text.
    """
    df[f'{column}_normalized'] = df[column].str.lower()
    df[f'{column}_normalized'] = df[f'{column}_normalized'].apply(lambda x: re.sub(f'[{string.punctuation}]', '', x))
    df[f'{column}_normalized'] = df[f'{column}_normalized'].apply(lambda x: re.sub(r'\d+', '', x))
    return df

def named_entity_recognition(df, column):
    """
    Perform Named Entity Recognition (NER) using spaCy.
    This method identifies named entities (e.g., persons, organizations) in the text.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of named entities and their labels.
    """
    df[f'{column}_entities'] = df[column].apply(lambda x: [(ent.text, ent.label_) for ent in nlp(x).ents])
    return df

def sentiment_analysis(df, column):
    """
    Perform sentiment analysis using NLTK's VADER.
    This method analyzes the sentiment of the text and returns a sentiment score.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    pd.DataFrame: Dataframe with an additional column of sentiment scores.
    """
    sia = SentimentIntensityAnalyzer()
    df[f'{column}_sentiment'] = df[column].apply(lambda x: sia.polarity_scores(x))
    return df

def tfidf_vectorization(df, column):
    """
    Perform TF-IDF vectorization on text.
    This method converts text into a matrix of TF-IDF features.

    Parameters:
    df (pd.DataFrame): The dataframe.
    column (str): The column containing text data.

    Returns:
    scipy.sparse.csr.csr_matrix, np.ndarray: TF-IDF feature matrix and feature names.
    """
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(df[column])
    return tfidf_matrix, vectorizer.get_feature_names_out()
