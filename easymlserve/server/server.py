from imp import reload
import uvicorn
from fastapi import Depends, FastAPI, Header, HTTPException

from easymlserve.service import EasyMLService


class EasyMLServer:

    def __init__(self,
                 service: EasyMLService,
                 api_keys=None,
                 uvicorn_args={}):
        self.app = FastAPI()
        self.api_keys = api_keys
        self.uvicorn_args=uvicorn_args

        if api_keys is not None:
            self.app.include_router(service.router, dependencies=[Depends(self._validate_api_key)])
        else:
            self.app.include_router(service.router)

    def _validate_api_key(self, x_api_key: str = Header(...)):
        """Check if 'x_api_key' in header is valid API key."""
        if x_api_key not in self.api_keys:
            raise HTTPException(status_code=400, detail='Invalid API Key')

    def deploy(self):
        uvicorn.run(self.app, **self.uvicorn_args)
