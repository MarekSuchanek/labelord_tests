# Testing list_repos command of labelord
# Every request there should have "?per_page=100&page=X"
# Content-Length doesn't have to be correct...


def test_list_normal(invoker, utils):
    # Successful list run should list 6 repositories, one on each
    # line (and each line ends with newline)
    invocation = invoker('--config', utils.config('config_token'),
                         'list_repos',
                         session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')
    repos01 = ['cvut/MI-PYT',
               'MarekSuchanek/PYT-TwitterWall',
               'MarekSuchanek/repocribro',
               'MarekSuchanek/repocribro-file',
               'MarekSuchanek/titanic',
               'MarekSuchanek/dotfiles']

    assert invocation.result.exit_code == 0
    assert len(lines) == 7 and lines[-1] == ''
    for repo in repos01:
        assert repo in lines


def test_list_no_token(invoker_norec):
    # In this test there is no config file, GITHUB_TOKEN envvar
    # nor --token option, so it should end with appropriate error
    invocation = invoker_norec('list_repos', isolated=True)
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 3
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'No GitHub token has been provided'


def test_list_bad_credentials(invoker, utils):
    # Different cassette is used - saying that bad credentials has
    # been used (invalid token)
    invocation = invoker('--config', utils.config('config_token'),
                         'list_repos',
                         session_expectations={'get': 1})
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 4
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'GitHub: ERROR 401 - Bad credentials'


def test_list_more_than_hundred(invoker, utils):
    # Different cassette is used - in this cassette are responses with
    # 335 repositories (really fat one)
    invocation = invoker('-c', utils.config('config_token'),
                         'list_repos',
                         session_expectations={'get': 4})
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 335 and lines[-1] == ''
    for i in range(334):
        assert 'MarekSuchanek/repo{}'.format(i) in lines
