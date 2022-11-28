from typing import Dict

from fastapi import APIRouter


class EasyMLService:
    """EasyMLServe Service base class every Service need to implement."""

    def __init__(self, route_args: Dict = {}):
        """Initialize EasyMLService base class.

        Args:
            route_args (Dict, optional): Arguments for FastAPI route. Defaults to {}.
        """
        self.router = APIRouter()
        self.router.add_api_route('/process', self.process,
                                  methods=['POST'], **route_args)
        self.route_args = route_args
        self.load_model()

    def load_model(self):
        """Optional load model routine."""
        pass

    def api_call(self, **kwargs) -> Dict:
        """Process incomming REST API call.

        Raises:
            NotImplementedError: If not implemented by child class.

        Returns:
            Dict: JSON response of API call.
        """
        raise NotImplementedError('TODO')
