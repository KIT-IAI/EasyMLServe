import base64
import io
import json
import os
from datetime import datetime
from typing import ByteString

import matplotlib.pyplot as plt
import numpy as np
import PIL

from skimage.color import label2rgb
from skimage.measure import label, regionprops

from easymlserve.ui import GradioEasyMLUI, QtEasyMLUI
from easymlserve.ui.type import File, Number, Plot

from api_schema import *


class CellSegmentationUI(GradioEasyMLUI):
    """Cell segmentation UI."""

    def prepare_request(self, image: ByteString) -> ImageSchema:
        image = PIL.Image.open(io.BytesIO(image))
        image = np.array(image)
        image_encoded = base64.b64encode(image)
        image_encoded = image_encoded.decode('utf-8')
        return {
            'dtype': str(image.dtype),
            'shape': list(image.shape),
            'image': image_encoded
        }

    def process_response(self,
                         request: ImageSchema,
                         response: ImageSchema
                        ) -> Plot:
        image = base64.decodebytes(str.encode(request['image']))
        image = np.frombuffer(image, dtype=getattr(np, request['dtype']))
        image = image.reshape(request['shape'])
        image = (image - image.min()) \
                / (image.max() - image.min())
        image = (image * 255).astype(np.uint8)

        instances = base64.decodebytes(str.encode(response['image']))
        instances = np.frombuffer(instances, dtype=getattr(np, response['dtype']))
        instances = instances.reshape(response['shape'])

        fig = plt.figure(figsize=(5, 4), dpi=300)
        plt.imshow(label2rgb(instances, image))
        fig.tight_layout()

        regions = regionprops(label(instances))

        response = {
            'instances': instances.tolist(),
            'num_instances': len(regions),
            'area': np.mean([region.area for region in regions])
        }
        os.makedirs('responses', exist_ok=True)
        file_name = datetime.now().strftime('%Y-%m-%d_%I-%M-%S_output.json')
        file_path = os.path.join('responses', file_name)
        with open(file_path, 'w') as file:
            json.dump(response, file)

        return fig, response['num_instances'], response['area'], file_path


if __name__ == '__main__':
    input_schema = {
        'image': File(name='Input Image')
    }
    output_schema = [
        Plot(name='Cell Segmentation'),
        Number(name='Number of Cells', dtype=int),
        Number(name='Mean Cell Size [px**2]', dtype=float),
        File(name='Response File')]
    gradio_interface_args = {
        'allow_flagging': False
    }
    gradio_launch_args = {
        'server_name': '0.0.0.0',
        'server_port': 8180
    }
    app = CellSegmentationUI(name='Cell Segmentation Example',
                             input_schema=input_schema,
                             output_schema=output_schema,
                             gradio_interface_args=gradio_interface_args,
                             gradio_launch_args=gradio_launch_args,
                             rest_api_port=8100)
    app.run()
