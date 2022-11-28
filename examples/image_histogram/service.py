import base64

import numpy as np

from easymlserve import EasyMLServer, EasyMLService

from api_schema import APIRequest, APIResponse


class HistogramImageService(EasyMLService):
    """Histogram calculation example service."""

    def process(self, request: APIRequest) -> APIResponse:
        """ Process REST API request and return histogram."""
        image = base64.decodebytes(str.encode(request.image))
        image = np.frombuffer(image, dtype=getattr(np, request.dtype))
        image = image.reshape(request.shape,)
        response = {'shape': image.shape}
        for color, channel in zip(['r', 'g', 'b'], range(3)):
            counts, bins = np.histogram(image[:, :, channel],
                                        bins=request.bins)
            rel_counts = counts / (np.prod(image.shape[:2]))
            response[color] = {
                'counts': counts.tolist(),
                'rel_counts': rel_counts.tolist(),
                'bins': bins.tolist()
            }
        return response


service = HistogramImageService()
server = EasyMLServer(service, uvicorn_args={'host': '0.0.0.0', 'port': 8000})
server.deploy()