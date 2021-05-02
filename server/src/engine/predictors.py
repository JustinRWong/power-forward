import pickle
import pandas as pd
# from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor

path_to_ml_models = 'engine/models/'

## load knn model from disk
knn_weekhour_model = DecisionTreeRegressor(random_state=0, max_depth=5)#KNeighborsRegressor(n_neighbors=2)#pickle.load(open(path_to_ml_models + 'knn_weekhour.sav', 'rb'))
x = pd.read_csv(path_to_ml_models + 'x_full.csv').drop('Unnamed: 0', axis=1)
y = pd.read_csv(path_to_ml_models + 'y_full.csv').drop('Unnamed: 0', axis=1)
knn_weekhour_model.fit(x, y)

##
single_loc_model = pickle.load(open(path_to_ml_models + 'Forest_Model.sav', 'rb'))

def apply_knn_weekhour_model(x_vector):

    weektime_series = []
    hours_per_week = 168
    timechunk = 1/24
    for i in range(hours_per_week):
        weektime_series.append(1 + i*timechunk)

    time = []
    rates = []
    for wt in weektime_series:
        x = x_vector + [wt]
        predicted_rate = knn_weekhour_model.predict([x])

        time.append(wt)
        rates.append(predicted_rate[0])

    # print('WE MADE IT TO THE END')
    return time, rates

def apply_single_location_predictor(x_vector):
    predicted_val = single_loc_model.predict(x_vector)
    return predicted_val
