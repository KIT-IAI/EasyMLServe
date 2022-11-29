import base64
import json
import os
from datetime import datetime

import numpy as np
import cv2
import matplotlib.pyplot as plt

from easymlserve.ui import GradioEasyMLUI, QtEasyMLUI
from easymlserve.ui.type import File, ImageFile, Number, Plot, Webcam
from api_schema import *


class HistogramUI(GradioEasyMLUI):
    """Histogram UI example."""

    def prepare_request(self, image: np.ndarray) -> APIRequest:
        """Prepare REST API request using input image and number of bins."""
        image_encoded = base64.b64encode(image)
        image_encoded = image_encoded.decode('utf-8')
        return {
            'dtype': str(image.dtype),
            'shape': list(image.shape),
            'image': image_encoded
        }

    def process_response(self,
                         request: APIRequest,
                         response: APIResponse
                        ) -> Plot:
        """Process REST API response by creating plots and file."""
        image = base64.decodebytes(str.encode(request['image']))
        image = np.frombuffer(image, dtype=getattr(np, request['dtype']))
        image = image.reshape(request['shape'])

        faces_image = image.copy()
        for face in response['faces']:
            x, y, w, h = face['x'], face['y'], face['w'], face['h']
            cv2.rectangle(faces_image, (x, y), (x+w, y+h), (255, 0, 0), 2)
        fig = plt.figure(figsize=(8, 5), dpi=300)
        plt.imshow(faces_image)
        plt.tight_layout()

        os.makedirs('responses', exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d_%I-%M-%S_output.json')
        file_path = os.path.join('responses', file_name)
        with open(file_path, 'w') as file:
            json.dump(response, file)

        return fig, len(response['faces']), file_path


if __name__ == '__main__':
    input_schema = {
        'image': Webcam(name='Input Image')
    }
    output_schema = [Plot(name='Detections'), Number(name='Number of Faces'), File()]
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