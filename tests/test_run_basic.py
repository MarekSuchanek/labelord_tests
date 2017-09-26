import pytest
import itertools


MODES = ['update', 'replace']
PRINTING = ['--verbose', '--quiet', '-q', '-v', None]


@pytest.mark.parametrize(
    ('mode', 'printing'),
    itertools.product(MODES, PRINTING)
)
def test_run_no_token(invoker_norec, mode, printing):
    # In this test there is no config file, GITHUB_TOKEN envvar
    # nor --token option, so it should end with appropriate error
    invocation = invoker_norec('run', mode, printing, isolated=True)
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 3
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'No GitHub token has been provided'


@pytest.mark.parametrize(
    ('mode', 'printing'),
    itertools.product(MODES, PRINTING)
)
def test_run_no_labels(invoker_norec, utils, mode, printing):
    # In this test there is a config with GitHub token
    # and repos defined, but not labels (not even empty)
    invocation = invoker_norec('--config', utils.config('config_nolabels'),
                               'run', mode, printing)
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 6
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'No labels specification has been found'


@pytest.mark.parametrize(
    ('mode', 'printing'),
    itertools.product(MODES, PRINTING)
)
def test_run_no_repos(invoker_norec, utils, mode, printing):
    # In this test there is a config with GitHub token
    # and labels defined, but not repos (not even empty)
    invocation = invoker_norec('-c', utils.config('config_norepos'),
                               'run', mode, printing)
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 7
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'No repositories specification has been found'
