import base64
import json
import os
from datetime import datetime

import matplotlib.pyplot as plt
import numpy as np
from api_schema import *

from easymlserve.ui import GradioEasyMLUI, QtEasyMLUI
from easymlserve.ui.type import File, ImageFile, Plot, Range, Webcam


class HistogramUI(GradioEasyMLUI):
    """Histogram UI example."""

    def prepare_request(self, image: np.ndarray, bins: int) -> APIRequest:
        """Prepare REST API request using input image and number of bins."""
        image_encoded = base64.b64encode(image)
        image_encoded = image_encoded.decode('utf-8')
        return {
            'dtype': str(image.dtype),
            'shape': list(image.shape),
            'image': image_encoded,
            'bins': bins
        }

    def process_response(self,
                         request: APIRequest,
                         response: APIResponse
                        ) -> Plot:
        """Process REST API response by creating plots and file."""
        fig = plt.figure(figsize=(8, 5), dpi=300)
        for color in ['r', 'g', 'b']:
            x = response[color]['bins']
            y = response[color]['rel_counts']
            x_idx = np.array([[i, i + 1] for i in range(len(x) - 1)])
            x = np.array(x)[x_idx].mean(axis=1)
            plt.plot(x, y, color=color)
        plt.tight_layout()

        os.makedirs('responses', exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d_%I-%M-%S_output.json')
        file_path = os.path.join('responses', file_name)
        with open(file_path, 'w') as file:
            json.dump(response, file)

        return fig, file_path


if __name__ == '__main__':
    input_schema = {
        'image': ImageFile(name='Input Image'),
        'bins': Range(10, 100, name='Number of Bins', dtype=int)
    }
    output_schema = [Plot(name='Image Historgram'), File()]
    gradio_interface_args = {
        'allow_flagging': False
    }
    gradio_launch_args = {
        'server_name': '0.0.0.0',
        'server_port': 8080
    }
    app = HistogramUI(name='Histogram Example',
                      input_schema=input_schema,
                      output_schema=output_schema,
                      gradio_interface_args=gradio_interface_args,
                      gradio_launch_args=gradio_launch_args,
                      rest_api_port=8000)
    app.run()