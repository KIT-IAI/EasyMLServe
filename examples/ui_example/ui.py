from easymlserve.ui import GradioEasyMLUI, QtEasyMLUI
from easymlserve.ui.type import *

from api_schema import *


class HistogramUI(GradioEasyMLUI):
    """
    This example is only an UI type example
    and, thus, does not process data as service.
    """
    pass


if __name__ == '__main__':
    input_schema = {
        'short_text': Text(name='ShortText'),
        'long_text': TextLong(name='LongText'),
        'long_text': Number(name='Number'),
        'range': Range(0, 100, int, name='RangeSlider'),
        'single_choice': SingleChoice(
            ['A', 'B', 'C'], name='SingleChoice'),
        'multiple_choice': MultipleChoice(
            ['A', 'B', 'C'], name='MultipleChoice'),
        'long_text': TextLong(name='LongText'),
        'file': File(name='File'),
        'image_file': ImageFile(name='ImageFile'),
        'csv_file': CSVFile(name='CSVFile')
    }
    output_schema = input_schema.values()
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