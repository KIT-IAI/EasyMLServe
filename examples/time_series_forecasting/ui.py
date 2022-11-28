import os
from datetime import datetime
from io import BytesIO
from typing import ByteString, List, Tuple

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

from easymlserve.ui import GradioEasyMLUI, QtEasyMLUI
from easymlserve.ui.type import CSVFile, MultipleChoice, Plot

from api_schema import *


class TSForecastingUI(GradioEasyMLUI):
    """Time series forecasting UI example."""

    def prepare_request(self,
                        models: List[str],
                        csv: ByteString) -> APIRequest:
        """Prepare REST API request using selected models and CSV."""
        df = pd.read_csv(BytesIO(csv))
        df.time = pd.to_datetime(df.time)
        df.time = df.time.astype(str)
        request = df[['time', 'energy']].to_dict('list')
        request['models'] = models
        return request

    def process_response(self,
                         request: APIRequest,
                         response: APIResponse
                        ) -> Tuple[Plot, Plot, CSVFile]:
        """Process REST API response by creating plots and returning CSV file."""
        figure_forecasts = plt.figure(figsize=(8, 4), dpi=300)
        original_time_series = pd.DataFrame()
        original_time_series['time'] = pd.to_datetime(request['time'])
        original_time_series['energy'] = request['energy']
        original_time_series.set_index('time', inplace=True)
        plt.plot(original_time_series.index, original_time_series.energy,
                 color='b', label='GroundTruth')
        forecast_time_series = []
        models = []
        for forecast in response['forecasts']:
            forecast_df = pd.DataFrame()
            forecast_df['time'] = pd.to_datetime(forecast['time'])
            forecast_df[forecast['model']] = forecast['energy']
            forecast_df.set_index('time', inplace=True)
            forecast_time_series.append(forecast_df)
            models.append(forecast['model'])
            plt.plot(forecast_df.index, forecast_df[forecast['model']],
                     label=forecast['model'])
        plt.xticks(rotation=45)
        plt.xlabel('Time[h]')
        plt.ylabel('Electrical Load [MW]')
        plt.title('24h Ahead Forecasting Results')
        figure_forecasts.legend()
        figure_forecasts.tight_layout()

        result_df = pd.concat([original_time_series, *forecast_time_series], axis=1)
        figure_error = plt.figure(figsize=(8, 4), dpi=300)
        for model in models:
            error = np.abs(result_df.energy - result_df[model])
            plt.plot(result_df.index, error, label=model)
        plt.xticks(rotation=45)
        plt.xlabel('Time[h]')
        plt.ylabel('Error [MW]')
        plt.title('24h Ahead Forecasting Error')
        figure_error.legend()
        figure_error.tight_layout()

        os.makedirs('responses', exist_ok=True)
        csv_file_name = datetime.now().strftime('%Y-%m-%d_%I-%M-%S_output.csv')
        csv_file_path = os.path.join('responses', csv_file_name)
        result_df.to_csv(csv_file_path)

        return figure_forecasts, figure_error, csv_file_path


if __name__ == '__main__':
    input_schema = {
        'models': MultipleChoice(['LR', 'SVR', 'RF'], name='Selected Models'),
        'csv': CSVFile(name='CSV File')
    }
    output_schema = [
        Plot(name='Forecasting Actual'),
        Plot(name='Forecasting Error'),
        CSVFile()
    ]
    gradio_interface_args = {
        'allow_flagging': False
    }
    gradio_launch_args = {
        'server_name': '0.0.0.0',
        'server_port': 8080
    }
    app = TSForecastingUI(name='Energy Time Series Forecasting',
                          input_schema=input_schema,
                          output_schema=output_schema,
                          gradio_interface_args=gradio_interface_args,
                          gradio_launch_args=gradio_launch_args,
                          rest_api_port=8000)
    app.run()