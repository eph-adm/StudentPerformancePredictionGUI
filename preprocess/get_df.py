import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt
import time
import pickle 

df = pd.read_csv('final_untransformed.csv')
columns = df.columns

label_feat = ['Eng3', 'Math3', 'Phy3', 'Chem3', 'Bio3']
df_inp = df.drop(label_feat, axis=1)
df_out = df[label_feat]


from sklearn.base import BaseEstimator, TransformerMixin

class DataFrameSelector(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names):
        self.attribute_names = attribute_names
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        return X[self.attribute_names].values

class OrdinalEncoder(BaseEstimator, TransformerMixin):
    def __init__(self, attribute_names, map_arr):
        self.attribute_names = attribute_names
        self.map_arr = map_arr
    def fit(self, X, y=None):
        return self
    def transform(self, X):
        X_tr = pd.DataFrame(X, columns=self.attribute_names)
        k = 0
        for i in self.attribute_names:
            X_tr[i] = X_tr[i].map(self.map_arr[k])
            k += 1
        return X_tr.values
    
class CustomLabelBinarizer(BaseEstimator, TransformerMixin):
    def __init__(self, sparse_output=False):
        self.sparse_output = sparse_output
    def fit(self, X, y=None):
        return self
    def transform(self, X, y=None):
        enc = LabelBinarizer(sparse_output=self.sparse_output)
        return enc.fit_transform(X)
    

map_arr = [
    {
        'Excellent': 4,
        'Very Good': 3,
        'Good': 2,
        'Satisfactory': 1   
    },
    {
        'Mother and Father': 6,
        'Mother Only': 5,
        'Father Only': 4,
        'Siblings': 3,
        'Other Relatives': 2,
        'I Live Alone': 1
    },
    {
        'More Than 20000': 4,
        '10000-20000': 3,
        '5000-10000': 2,
        'Less Than 5000': 1
    },
    {
        'PhD': 7,
        'Masters': 6,
        'Degree': 5,
        'Diploma': 4,
        'High School': 3,
        'High SchoolDropout': 2,
        'No Education': 1
    },
    {
        'Yes': 2,
        'No': 1
    },
    {
        '3.5-4': 4,
        '3-3.5': 3,
        '2.5-3': 2,
        '2-2.5': 1    
    }
]

from sklearn.pipeline import FeatureUnion, Pipeline
from sklearn.preprocessing import StandardScaler, Imputer, LabelBinarizer, OneHotEncoder
from sklearn_pandas import CategoricalImputer


num_attribs = ['Age', 'Eng1', 'Math1', 'Phy1', 'Chem1', 'Bio1', 'Eng2', 'Math2', 'Phy2', 'Chem2', 'Bio2']
cat_attribs1 = ['Sex']
cat_attribs2 = ['Q7']
cat_attribs3 = ['Q8']
ord_attribs = ['Q1', 'Q2', 'Q3', 'Q4', 'Q5', 'Q6']

num_pipeline = Pipeline([
    ('selector', DataFrameSelector(num_attribs)),
    ('imputer', Imputer(strategy="median")),
    ('std_scaler', StandardScaler()),
])
cat_pipeline = Pipeline([
    ('selector', DataFrameSelector(cat_attribs1)),
    ('imputer', CategoricalImputer()),
    ('label_binarizer', CustomLabelBinarizer()),
])
cat_pipeline2 = Pipeline([
    ('selector', DataFrameSelector(cat_attribs2)),
    ('imputer', CategoricalImputer()),
    ('label_binarizer', CustomLabelBinarizer()),
])
cat_pipeline3 = Pipeline([
    ('selector', DataFrameSelector(cat_attribs3)),
    ('imputer', CategoricalImputer()),
    ('label_binarizer', CustomLabelBinarizer()),
])
ord_pipeline = Pipeline([
    ('selector', DataFrameSelector(ord_attribs)),
    ('imputer', CategoricalImputer()),
    ('encoder', OrdinalEncoder(ord_attribs, map_arr)),
])
full_pipeline = FeatureUnion(transformer_list=[
    ("num_pipeline", num_pipeline),
    ("cat_pipeline1", cat_pipeline),
    ("cat_pipeline2", cat_pipeline2),
    ("cat_pipeline3", cat_pipeline3),
    ("ord_pipeline", ord_pipeline)
])


x = full_pipeline.fit_transform(df_inp)
y = df_out.values

for i in range(y.shape[0]):
    for j in range(y.shape[1]):
        if y[i, j] >=0 and y[i, j] < 50:
            y[i, j] = 0
        else:
            y[i, j] = 1
y = y.astype(int)



y_eng = y[:, 0]
y_math = y[:, 1]
y_phy = y[:, 2]
y_chem = y[:, 3]
y_bio = y[:, 4]


_, X_eng, _, y_eng = train_test_split(x, y_eng, test_size=.3, random_state=0, stratify=y_eng)
_, X_math, _, y_math = train_test_split(x, y_math, test_size=.3, random_state=0, stratify=y_math)
_, X_phy, _, y_phy = train_test_split(x, y_phy, test_size=.3, random_state=0, stratify=y_phy)
_, X_chem, _, y_chem = train_test_split(x, y_chem, test_size=.3, random_state=0, stratify=y_chem)
_, X_bio, _, y_bio = train_test_split(x, y_bio, test_size=.3, random_state=0, stratify=y_bio)


columns = columns[0:20]


def get_str(data):
    if data[0] == 0:
        return "Fail"
    else:
        return "Pass"



from sklearn.metrics import accuracy_score
def predict(inp):
    #inp = get_data()
    pred_res = []
    probab_res = []
    dummy_df = pd.DataFrame(df_inp.values, columns=columns)
    #dummy_df.loc[-1] = inp
    dummy_df = dummy_df.append(pd.Series(inp, index=dummy_df.columns), ignore_index=True)
    x_ = full_pipeline.fit_transform(dummy_df)
    xi = x_[-1, :]
    xi = xi.reshape(1, -1)
    del dummy_df
    eng_model = pickle.load(open('finalized_model_eng.sav', 'rb'))
    math_model = pickle.load(open('finalized_model_math.sav', 'rb'))
    phy_model = pickle.load(open('finalized_model_phy.sav', 'rb'))
    chem_model = pickle.load(open('finalized_model_chem.sav', 'rb'))
    bio_model = pickle.load(open('finalized_model_bio.sav', 'rb'))

    pred_res.append(get_str(eng_model.predict(xi)))
    pred_res.append(get_str(math_model.predict(xi)))
    pred_res.append(get_str(phy_model.predict(xi)))
    pred_res.append(get_str(chem_model.predict(xi)))
    pred_res.append(get_str(bio_model.predict(xi)))

    probab_res.append(accuracy_score(y_eng, eng_model.predict(X_eng)))
    probab_res.append(accuracy_score(y_math, eng_model.predict(X_math)))
    probab_res.append(accuracy_score(y_phy, eng_model.predict(X_phy)))
    probab_res.append(accuracy_score(y_chem, eng_model.predict(X_chem)))
    probab_res.append(accuracy_score(y_bio, eng_model.predict(X_bio)))
 
    return pred_res, probab_res