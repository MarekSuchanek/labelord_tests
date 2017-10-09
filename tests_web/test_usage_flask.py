from werkzeug.test import Client
from werkzeug.wrappers import BaseResponse
import os


def test_flask_run(utils):
    # Use Werkzeug as flask run does but use it
    # to test (flask run uses run_simple() instead)
    os.environ['LABELORD_CONFIG'] = utils.config('config_3repos')
    from labelord import app
    client = Client(app, BaseResponse)
    result = client.get('/')
    assert result.status_code == 200
    assert 'master-to-master' in result.data.decode('utf-8')

    page = result.data.decode('utf-8')
    assert 'master-to-master' in page
    assert 'MarekSuchanek/pyplayground' in page
    assert 'MarekSuchanek/repocribro' in page
    assert 'MarekSuchanek/labelord' not in page
    assert 'MarekSuchanek/maze' in page
