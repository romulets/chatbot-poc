import pandas as pd
import spacy
import contractions

from sklearn.preprocessing import FunctionTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline

nlp = spacy.load("en_core_web_sm")


def retrieve_tags(tag_model, raw_data_set, sentence): 
    sentence_series = pd.Series([_lemmatize(sentence)])

    prediction = tag_model.predict(sentence_series)
    tag = raw_data_set.query("tag_code == " + str(prediction[0]))["tag"].unique().astype(str)[0]

    print("DEBUG: Tag", tag)

    return [tag]

def _lemmatize(sentence):
    sentence = contractions.fix(sentence)

    doc = nlp(sentence)
    lemma_list = [token.lemma_ for token in doc if token.is_alpha]
    return ' '.join(lemma_list)

def lemmatize_transformer(X):
    return X.apply(_lemmatize)

def train_model(file):
    print("DEBUG: Training Model....")

    #read file
    raw_data_set = pd.read_csv(file)
    # rename columns
    raw_data_set.columns = ["tag", "text"]
    # drop null
    raw_data_set = raw_data_set.dropna()
    # transform tags to categorues
    raw_data_set["tag"] = pd.Categorical(raw_data_set["tag"])
    # get codes
    raw_data_set["tag_code"] = raw_data_set["tag"].cat.codes

    # Set the subject
    X = raw_data_set["text"]
    # Set the goal
    y = raw_data_set["tag_code"]

    # Create a model
    model = make_pipeline(
        FunctionTransformer(func=lemmatize_transformer, validate=False),
        CountVectorizer(), 
        SGDClassifier(loss="log")
    )

    # Split data
    X_train, X_test, y_train, y_text = train_test_split(X, y, test_size=0.2)

    # Train
    model.fit(X, y)

    # Score
    print("DEBUG: Model Score", model.score(X_test, y_text))
    print("------------------\n")

    return (model, raw_data_set)


if __name__ == "__main__":
    (model, data_set) = train_model("./resources/sentence-tags-training-data.csv")
    while True:
        sentence = str(input("Sentence: "))    
        category = retrieve_tags(model, data_set, sentence)
        print("Tag: ", category)
        print("DEBUG: ", _lemmatize(sentence))
        print()