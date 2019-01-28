from sklearn.naive_bayes import MultinomialNB
from sklearn.linear_model import SGDClassifier
from sklearn.preprocessing import LabelEncoder
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import classification_report, confusion_matrix


def load_data(path):
    X = []
    y = []
    for text in open(path, encoding='utf8').readlines():
        words = text.strip().split()
        X.append(' '.join(words[1:]))
        y.append(words[0])
    return X, y


def nb(X, y):
    text_clf_svm = Pipeline(
        [('vect', CountVectorizer(max_features=None, min_df=10, max_df=0.9)), ('tfidf', TfidfTransformer()),
         ('clf', MultinomialNB())])
    text_clf_svm.fit(X, y)
    return text_clf_svm


def svm(X, y):
    text_clf_svm = Pipeline(
        [('vect', CountVectorizer(max_features=None, min_df=10, max_df=0.9)), ('tfidf', TfidfTransformer()),
         ('clf', LinearSVC())])
    text_clf_svm.fit(X, y)
    return text_clf_svm

def sgd(X, y):
    text_clf_svm = Pipeline(
        [('vect', CountVectorizer(max_features=None, min_df=10, max_df=0.9)), ('tfidf', TfidfTransformer()),
         ('clf', SGDClassifier())])
    text_clf_svm.fit(X, y)
    return text_clf_svm


def evaluate(sk_model, X, y):
    if sk_model is None:
        raise ValueError('Model is None. Call train method')
    y_pred = sk_model.predict(X)
    print(confusion_matrix(y, y_pred))
    print(classification_report(y, y_pred))


if __name__ == '__main__':
    X_train, y_train = load_data('data/train.txt')
    X_test, y_test = load_data('data/test.txt')
    lb = LabelEncoder()
    lb.fit(y_train)
    y_train = lb.transform(y_train)
    y_test = lb.transform(y_test)

    model = sgd(X_train, y_train)
    evaluate(model, X_test, y_test)
    print(lb.classes_)
