import requests

import pandas as pd
import matplotlib.pyplot as plt


OPSD_URL = 'https://data.open-power-system-data.org/time_series/2020-10-06/time_series_60min_singleindex.csv'
OPSD_KEEP = [
    'utc_timestamp',
    'DE_load_actual_entsoe_transparency',
    'DE_solar_capacity',
    'DE_solar_generation_actual',
    'DE_wind_capacity',
    'DE_wind_generation_actual',
]
WEATHER_URL = 'https://data.open-power-system-data.org/weather_data/2020-09-16/weather_data.csv'
WEATHER_KEEP = [
    'utc_timestamp',
    'DE_temperature'
]


def download(url, output):
    r = requests.get(url)
    with open(output, "wb") as file:
        file.write(r.content)


def load_csv(path):
    with open(path, 'rb') as file:
        pkl = pd.read_csv(file)
        file.close()
    return pkl


def create_example_requests(opsd_frame):
    energy_key = 'DE_load_actual_entsoe_transparency'
    year = 2019
    for month in range(1, 13):
        frame = pd.DataFrame()
        frame['time'] = opsd_frame.loc[f'{year}-{month:01}'].index
        frame['energy'] = opsd_frame.loc[f'{year}-{month:01}'][energy_key].values
        frame.to_csv(f'{year}-{month}.csv', index=False)
    year = 2020
    for month in range(1, 10):
        frame = pd.DataFrame()
        frame['time'] = opsd_frame.loc[f'{year}-{month:01}'].index
        frame['energy'] = opsd_frame.loc[f'{year}-{month:01}'][energy_key].values
        frame.to_csv(f'{year}-{month}.csv', index=False)


def main():
    download(OPSD_URL, 'opsd.csv')
    opsd = load_csv('opsd.csv')
    opsd = opsd[OPSD_KEEP]
    opsd['utc_timestamp'] = pd.to_datetime(opsd['utc_timestamp'])
    opsd.set_index('utc_timestamp', inplace=True)

    download(WEATHER_URL, 'weather.csv')
    weather = load_csv('weather.csv')
    weather = weather[WEATHER_KEEP]
    weather['utc_timestamp'] = pd.to_datetime(weather['utc_timestamp'])
    weather.set_index('utc_timestamp', inplace=True)

    opsd_frame = opsd.join(weather)
    opsd_frame.to_csv('opsd_and_weather.csv')
    print(opsd_frame.describe())
    print(opsd_frame)

    create_example_requests(opsd_frame)

    for column in opsd_frame.columns:
        plt.plot(opsd_frame.index, opsd_frame[column])
        plt.savefig(f'{column}.png')
        plt.close()


if __name__ == '__main__':
    main()
