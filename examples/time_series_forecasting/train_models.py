import os
import pickle

import numpy as np
import pandas as pd

from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.svm import SVR


def load_dataset():
    data_path = os.path.join('data', 'opsd_and_weather.csv')
    csv_df = pd.read_csv(data_path)
    dataset = pd.DataFrame()
    dataset['time'] = pd.to_datetime(csv_df['utc_timestamp'])
    dataset['energy'] = csv_df['DE_load_actual_entsoe_transparency']
    return dataset


def clean_dataset(dataset):
    dataset = dataset.iloc[1:]
    dataset.reset_index(inplace=True)
    for column in dataset:
        if np.isnan(dataset[column]).sum() > 0:
            raise Exception('Please clean all nan data.')
    return dataset


def create_features(dataset):
    time = dataset['time']
    energy = dataset['energy'].values

    energy_mean = 55492
    energy_std = 10015
    energy_normalized = (energy - energy_mean) / energy_std
    target = energy_normalized[47:]

    features = {}
    for i in range(24):
        features[f'lag_{i}'] = energy_normalized[23 - i:-24 - i]
    features['weekend'] = (time[47:].dt.weekday >= 5).values
    features['hour_sin'] = np.sin(2 * np.pi * time[23:-24].dt.hour / 24).values
    features['hour_cos'] = np.cos(2 * np.pi * time[23:-24].dt.hour / 24).values
    features['dayofyear_sin'] = np.sin(2 * np.pi * time[23:-24].dt.dayofyear / 366).values
    features['dayofyear_cos'] = np.cos(2 * np.pi * time[23:-24].dt.dayofyear / 366).values

    features_df = pd.DataFrame(features)
    features_df['time'] = time[23:-24].reset_index(drop=True)
    features_df.set_index('time', inplace=True)
    target_df = pd.DataFrame(target, index=time[47:])

    return features_df, target_df


def split_features(features, target):
    train_idx = features.index.year < 2019 
    train_x = features.iloc[train_idx]
    test_x = features.iloc[~train_idx]
    train_y = target.iloc[train_idx]
    test_y = target.iloc[~train_idx]
    return train_x, train_y, test_x, test_y


def train_models(train_x, train_y):
    models = [
        ('LR', LinearRegression()),
        ('SVR', SVR()),
        ('RF', RandomForestRegressor()),
    ]
    for name, model in models:
        print(f'Training {name} ...', end=' ')
        model.fit(train_x.values, train_y.values.flatten())
        print(f'Done!')

        os.makedirs('models', exist_ok=True)
        model_path = os.path.join('models', f'{name.lower()}.pkl')
        with open(model_path, 'wb') as file:
            pickle.dump(model, file)

    return models


def evaluate_models(test_x, test_y, models):
    for name, model in models:
        prediction = model.predict(test_x.values)
        error = np.abs(prediction - test_y.values.flatten())
        mae = error.mean()
        mse = np.square(error).mean()
        print(f'{name:4}  -  MAE: {mae:.3f}  MSE: {mse:.3f}')


if __name__ == '__main__':
    dataset = load_dataset()
    dataset = clean_dataset(dataset)
    features, target = create_features(dataset)
    train_x, train_y, test_x, test_y = split_features(features, target)
    models = train_models(train_x, train_y)
    evaluate_models(test_x, test_y, models)
