import os
import pickle

import numpy as np
import pandas as pd

from fastapi import HTTPException

from easymlserve import EasyMLServer, EasyMLService

from api_schema import *


class TimeSeriesForecastingService(EasyMLService):
    """Service to forecast time series using multiple pretrained models."""

    def load_model(self):
        """Load pretrained models."""
        models = {}
        for model_name in ['LR', 'SVR', 'RF']:
            model_path = os.path.join('models', model_name.lower() + '.pkl')
            with open(model_path, 'rb') as file:
                model = pickle.load(file)
            models[model_name] = model
        self.models = models

    def get_features(self, df):
        """Calculate and return features."""
        features = {}
        time = df['time']
        forecast_time = df['time'] + pd.Timedelta('1d')
        energy_normalized = df['energy'].values
        for i in range(24):
            if i == 0:
                features[f'lag_{i}'] = energy_normalized[23 - i:]
            else:
                features[f'lag_{i}'] = energy_normalized[23 - i:-i]
        features['weekend'] = (forecast_time[23:].dt.weekday >= 5).values
        features['hour_sin'] = np.sin(2 * np.pi * time[23:].dt.hour / 24).values
        features['hour_cos'] = np.cos(2 * np.pi * time[23:].dt.hour / 24).values
        features['dayofyear_sin'] = np.sin(2 * np.pi * time[23:].dt.dayofyear / 366).values
        features['dayofyear_cos'] = np.cos(2 * np.pi * time[23:].dt.dayofyear / 366).values
        return pd.DataFrame(features, index=time[23:])

    def process(self, request: APIRequest) -> APIResponse:
        """Process time series and return forecasts."""
        df = pd.DataFrame()
        df['time'] = pd.to_datetime(request.time)
        df['energy'] = (np.array(request.energy) - 55492) / 10015
        features = self.get_features(df)
        forecasts = []
        for model in request.models:
            if model in self.models:
                prediction = self.models[model].predict(features.values)
                prediction = prediction * 10015 + 55492
            else:
                raise HTTPException(404, 'Unkown model')
            time = pd.to_datetime(features.index) + pd.Timedelta('1d')
            forecasts.append({
                'model': model,
                'time': time.astype(str).to_list(),
                'energy': prediction.tolist()
            })
        return APIResponse(forecasts=forecasts)


if __name__ == '__main__':
    service = TimeSeriesForecastingService()
    server = EasyMLServer(service, uvicorn_args={'host': '0.0.0.0'})
    server.deploy()
