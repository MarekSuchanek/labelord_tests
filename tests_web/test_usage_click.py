import pytest


def test_click_run_server(invoker, utils):
    # Test if click command is implemented and use app.run(...)
    # to run the server, then test if the app is running fine
    from labelord import app

    def mock_run(host, port, debug, *opts):
        print('Host:', host)
        print('Port:', port)
        print('Debug:', debug)
        print('Opts:', opts)

    app.run = mock_run  # overwrite real app.run with dummy function
    invocation = invoker('--config', utils.config('config_3repos'),
                         'run_server', '--debug', '--host', '127.66.66.66',
                         '--port', '5666')
    lines = invocation.result.output.split('\n')
    assert 'Host: 127.66.66.66' in lines
    assert 'Port: 5666' in lines
    assert 'Debug: True' in lines

    # Now test the app with loaded config_3repos
    client = app.test_client()
    result = client.get('/')
    assert result.status_code == 200

    page = result.data.decode('utf-8')
    assert 'master-to-master' in page
    assert 'MarekSuchanek/pyplayground' in page
    assert 'MarekSuchanek/repocribro' in page
    assert 'MarekSuchanek/labelord' not in page
    assert 'MarekSuchanek/maze' in page


@pytest.mark.parametrize('isolated', [True, False])
def test_click_run_server_help(invoker_norec, isolated):
    # There must be standard click help describing options and args
    #
    # Local default config is not required (no token for help is OK)!
    #
    # It could look like this (types and help texts may differ):
    # Usage: labelord.py run_server [OPTIONS]
    #
    #   Run master-to-master replication server.
    #
    # Options:
    #  -h, --host TEXT     The interface to bind to.
    #  -p, --port INTEGER  The port to bind to.
    #  -d, --debug         Turns on DEBUG mode.
    #  --help              Show this message and exit
    invocation = invoker_norec('run_server', '--help', isolated=isolated)

    assert invocation.result.exit_code == 0
    assert '-h, --host' in invocation.result.output
    assert '-p, --port' in invocation.result.output
    assert '-d, --debug' in invocation.result.output
    assert '--help' in invocation.result.output
