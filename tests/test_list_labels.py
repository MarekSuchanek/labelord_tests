# Testing list_labels command of labelord
# Every request there should have "?per_page=100&page=X"
# Content-Length doesn't have to be correct...


def test_list_normal(invoker, utils):
    # Successful list run should list 12 labels, one on each
    # line with color (and each line ends with newline)
    invocation = invoker('--config', utils.config('config_token'),
                         'list_labels', 'MarekSuchanek/repo1',
                         session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')
    labels01 = ['#ee0701 bug',
                '#b495a9 core idea',
                '#cccccc duplicate',
                '#84b6eb enhancement',
                '#bfdadc experience',
                '#b495a9 extension idea',
                '#128A0C help wanted',
                '#cccccc invalid',
                '#cccccc on hold',
                '#84b6eb optimization',
                '#cc317c question',
                '#cccccc wontfix']

    assert invocation.result.exit_code == 0
    assert len(lines) == 13 and lines[-1] == ''
    for label in labels01:
        assert label in lines


def test_list_no_token(invoker_norec):
    # In this test there is no config file, GITHUB_TOKEN envvar
    # nor --token option, so it should end with appropriate error
    invocation = invoker_norec('list_labels', 'MarekSuchanek/repo1',
                               isolated=True)
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 3
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'No GitHub token has been provided'


def test_list_bad_credentials(invoker, utils):
    # Different cassette is used - saying that bad credentials has
    # been used (invalid token)
    invocation = invoker('-c', utils.config('config_token'),
                         'list_labels', 'MarekSuchanek/repo1',
                         session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 4
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'GitHub: ERROR 401 - Bad credentials'


def test_list_unexisting_repo(invoker, utils):
    # Repository MarekSuchanek/repo2 does not exist (or is hidden for
    # the given token)!
    invocation = invoker('--config', utils.config('config_token'),
                         'list_labels', 'MarekSuchanek/repo2',
                         session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 5
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'GitHub: ERROR 404 - Not Found'


def test_list_more_than_hundred(invoker, utils):
    # Different cassette is used - in this cassette are responses with
    # 154 labels (really fat one)
    invocation = invoker('-c', utils.config('config_token'),
                         'list_labels', 'MarekSuchanek/repo3',
                         session_expectations={'get': 2})
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 155 and lines[-1] == ''
    for i in range(154):
        assert '#ABC{} label{}'.format(i+100, i) in lines
