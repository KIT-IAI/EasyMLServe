import os
import base64

import numpy as np
import torch

from easymlserve import EasyMLServer, EasyMLService

from api_schema import ImageSchema


class SegmentationService(EasyMLService):
    """Exemplary cell segmentation service."""

    def __init__(self, torch_device='cpu', **kwargs):
        self.torch_device = torch_device
        super().__init__(**kwargs)

    def load_model(self):
        self.model = torch.load(os.path.join('model', 'model.pkl'))
        self.model = self.model.double().to(self.torch_device)

    def process(self, request: ImageSchema) -> ImageSchema:
        """ TODO """
        image = base64.decodebytes(str.encode(request.image))
        image = np.frombuffer(image, dtype=getattr(np, request.dtype))
        image = image.reshape(request.shape)
        if len(image.shape) > 2:
            image = image[:, :, 0].astype(np.double)
        else:
            image = image.astype(np.double)
        norm_image = (image - np.min(image)) \
                   / (np.max(image) - np.min(image))
        tensor_image = torch.from_numpy(norm_image)[None, None, ...]
        distance_map = self.model(tensor_image.to(self.torch_device)).to('cpu')
        instances = self.model.post_pro.process(
            distance_map.squeeze().detach().numpy(),
            None
        )
        image_encoded = base64.b64encode(instances)
        image_encoded = image_encoded.decode('utf-8')
        return {
            'dtype': str(instances.dtype),
            'shape': list(instances.shape),
            'image': image_encoded
        }


if __name__ == '__main__':
    service = SegmentationService(torch_device='cuda')
    server = EasyMLServer(service, uvicorn_args={'host': '0.0.0.0', 'port': 8100})
    server.deploy()