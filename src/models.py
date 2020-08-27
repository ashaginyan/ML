from sklearn.linear_model import LogisticRegression
import pickle
from sklearn.metrics import precision_score, recall_score, f1_score, accuracy_score
from xgboost import XGBClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

def preprocess_data(data, model_type='strict', process_type='train'):
    if process_type == 'train':
        for idx in data.index:
            if data.loc[idx, 'result'] == -1:
                data.loc[idx, 'result'] = 0

    if model_type == 'strict' or model_type == 'middle':
        if process_type == 'train':
            y = data[['result']]
            y = 1 - y
            X = data.drop(columns=['result'])
        else:
            X = data
            return X
    elif model_type=='risk':
        if process_type == 'train':
            y = data[['result']]
            X = data.drop(columns=['result'])
        else:
            X = data
            return X
    else:
        print('Wrong model type')
        return
    return X, y

def get_score(y_true, y_pred):
    return precision_score(y_true, y_pred), recall_score(y_true, y_pred), \
           f1_score(y_true, y_pred), accuracy_score(y_true, y_pred)

class Strict_model:
    def __init__(self, class_weight={0:1, 1:1}):
        self.model = LogisticRegression(class_weight=class_weight)

    def train(self, data):
        X, y = preprocess_data(data, model_type='strict', process_type='train')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
        self.y_test = y_test
        self.model.fit(X_train, y_train.values.ravel())
        filename = 'strict_model.sav'
        pickle.dump(self.model, open(filename, 'wb'))
        self.y_pred_test = self.model.predict(X_test)

    def test(self, data):
        X = preprocess_data(data, model_type='strict', process_type='test')
        filename = 'strict_model.sav'
        self.model = pickle.load(open(filename, 'rb'))
        return self.model.predict(X), self.model.predict_proba(X)


class Middle_model:
    def __init__(self, n_estimators=1000, learning_rate=0.1, max_depth=8):
        self.model = XGBClassifier(n_estimators=n_estimators, max_depth=max_depth, learning_rate=learning_rate) # XGBClassifier(verbosity=1, n_estimators=n_estimators, learning_rate=learning_rate, max_depth=max_depth)

    def train(self, data):
        X, y = preprocess_data(data, model_type='middle', process_type='train')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
        self.y_test = y_test
        self.y_true = y
        self.model.fit(X_train, y_train.values.ravel())
        pickle.dump(self.model, open("middle_model.pickle.dat", "wb"))
        self.y_pred_test = self.model.predict(X_test)

    def test(self, data):
        self.model = pickle.load(open("middle_model.pickle.dat", "rb"))
        X = preprocess_data(data, model_type='middle', process_type='test')
        y_pred = self.model.predict(X)
        return y_pred

class Risk_model:
    def __init__(self, class_weight={0:1, 1:2}):
        self.model = LogisticRegression(class_weight=class_weight)

    def train(self, data):
        X, y = preprocess_data(data, model_type='risk', process_type='train')
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.10)
        self.y_test = y_test
        self.y_true = y
        self.model.fit(X_train, y_train.values.ravel())
        pickle.dump(self.model, open("risk_model.sav", "wb"))
        self.y_pred_test = self.model.predict(X_test)


    def test(self, data):
        X = preprocess_data(data, model_type='risk', process_type='test')
        filename = 'risk_model.sav'
        self.model = pickle.load(open(filename, 'rb'))
        return self.model.predict(X), self.model.predict_proba(X)






