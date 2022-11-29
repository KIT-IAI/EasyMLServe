import os
import base64

import numpy as np
import cv2

from easymlserve import EasyMLServer, EasyMLService

from api_schema import APIRequest, APIResponse


class HistogramImageService(EasyMLService):
    """Histogram calculation example service."""

    def load_model(self):
        model_path = os.path.join('model', 'model.xml')
        self.model = cv2.CascadeClassifier(model_path)

    def process(self, request: APIRequest) -> APIResponse:
        """ Process REST API request and return histogram."""
        image = base64.decodebytes(str.encode(request.image))
        image = np.frombuffer(image, dtype=getattr(np, request.dtype))
        image = image.reshape(request.shape)
        image_grayscale = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        detections = self.model.detectMultiScale(image_grayscale, 1.1, 4)
        response = {'faces': []}
        for (x, y, w, h) in detections:
            detection = {
                'x': int(x),
                'y': int(y),
                'w': int(w),
                'h': int(h),
            }
            response['faces'].append(detection)
        return response


service = HistogramImageService()
server = EasyMLServer(service, uvicorn_args={'host': '0.0.0.0', 'port': 8000})
server.deploy()