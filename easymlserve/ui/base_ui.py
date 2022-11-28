from typing import Dict, Iterable, List

import requests


class BaseEasyMLUI:
    """Basic UI class for every UI implementation."""

    def __init__(self,
                 name: str,
                 input_schema: Dict,
                 output_schema: List,
                 rest_api_host: str = '127.0.0.1',
                 rest_api_port: int = 8080,
                 rest_api_protocol: str = 'http',
                 **kwargs):
        """Initialize basic UI elements.

        Args:
            name (str): Name of the UI
            input_schema (Dict): UI type dict defining input schema.
            output_schema (List): UI type lst defining output_schema.
            rest_api_host (str, optional): REST API server address. Defaults to '127.0.0.1'.
            rest_api_port (int, optional): REST API server Port. Defaults to 8080.
            rest_api_protocol (str, optional): REST API server protocoll. Defaults to 'http'.
        """
        self.name = name
        self.input_schema = input_schema
        self.output_schema = output_schema
        self.rest_api_host = rest_api_host
        self.rest_api_port = rest_api_port
        self.rest_api_protocol = rest_api_protocol
        if not isinstance(self.output_schema, Iterable):
            self.output_schema = [self.output_schema]

    def call_process_api(self, request: Dict) -> Dict:
        """Call REST API server interface with request dict.

        Args:
            request (Dict): Request to send to REST API server.

        Returns:
            Dict: Response of REST API server.
        """
        r = requests.post(
            f'{self.rest_api_protocol}://'
            f'{self.rest_api_host}:{self.rest_api_port}'
            '/process',
            json=request
        )
        return r.json()

    def clicked(self, **kwargs) -> List:
        """UI clicked event to prepare and send REST API request.

        Returns:
            List: Results of processed REST API call to display.
        """
        request = self.prepare_request(**kwargs)
        response = self.call_process_api(request)
        return self.process_response(request, response)

    def prepare_request(self, **kwargs) -> Dict:
        """Prepare UI input for REST API request.

        Raises:
            NotImplemented: If not implemented by child UI.

        Returns:
            Dict: Prepared REST API request to send.
        """
        raise NotImplemented(
            'Every service has to implement a prepare_request method.')

    def process_response(self, request: Dict, response: Dict) -> List:
        """Process REST API response and return results to display.

        Args:
            request (Dict): REST API request which was send.
            response (Dict): REST API response which should be displayed.

        Raises:
            NotImplemented: If not implemented by child UI.

        Returns:
            List: Results to display at UI output schema.
        """
        raise NotImplemented(
            'Every service has to implement a process_response method.')

    def run(self):
        raise NotImplemented('Every UI has to implement a run method.')
