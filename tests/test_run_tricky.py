

def test_color_case_sensitivity(invoker, utils):
    # Color HEX can be mixed cased and it is OK.
    # Although it is not a different color, you
    # should be able to change it via labelord!
    # eEeEeE != EEEEEE in labelord (let GitHub
    # decide and handle that...)
    # repo4 contains label0 with color eEeEeE
    invocation = invoker('-c', utils.config('config_color'),
                         'run', 'update', '--verbose',
                         session_expectations={
                             'get': 1,
                             'post': 0,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 3 and lines[-1] == ''
    assert '[UPD][SUC] MarekSuchanek/repo4; label0; EEEEEE' in lines
    assert lines[-2] == '[SUMMARY] 1 repo(s) updated successfully'


def test_label_case_sensitivity(invoker, utils):
    # Label names are case insensitive, so if
    # there is same name with different case in
    # the config, you should update the name
    # instead of creating new!
    # repo4 contains label0 but should update to
    # LaBeL0 now...
    invocation = invoker('-c', utils.config('config_label'),
                         'run', 'update', '--verbose',
                         session_expectations={
                             'get': 1,
                             'post': 0,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 3 and lines[-1] == ''
    assert '[UPD][SUC] MarekSuchanek/repo4; LaBeL0; EEEEEE' in lines
    assert lines[-2] == '[SUMMARY] 1 repo(s) updated successfully'


def test_change_not_owned(invoker, utils):
    # Can read public repo but cannot change labels
    # leads to 404 - Not Found on the change
    invocation = invoker('-c', utils.config('config_notowned'),
                         'run', 'update', '--verbose',
                         session_expectations={
                             'get': 1,
                             'post': 1,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 3 and lines[-1] == ''
    assert '[ADD][ERR] requests/requests; SWAG; FF66CC; 404 - Not Found' in lines
    assert lines[-2] == '[SUMMARY] 1 error(s) in total, please check log above'


def test_help(invoker_norec):
    # There must be standard click help describing options
    # and commands (you should write description for each)
    # It should look like this:
    # Usage: labelord.py [OPTIONS] COMMAND [ARGS]...
    #
    # Options:
    #   -c, --config FILENAME  Path of the auth config file.
    #   -t, --token TEXT       GitHub API token.
    #   --version              Show the version and exit.
    #   --help                 Show this message and exit.
    #
    # Commands:
    #   list_labels  Listing labels of desired repository.
    #   list_repos   Listing accessible repositories.
    #   run          Run labels processing.
    invocation = invoker_norec('--help')

    assert invocation.result.exit_code == 0
    assert '-c, --config' in invocation.result.output
    assert '-t, --token' in invocation.result.output
    assert '--version' in invocation.result.output
    assert '--help' in invocation.result.output
    assert 'list_labels' in invocation.result.output
    assert 'list_repos' in invocation.result.output
    assert 'run' in invocation.result.output


def test_help_list_labels(invoker_norec):
    # There must be standard click help describing options
    # and commands (you should write description for each)
    # It should look like this:
    # Usage: labelord.py list_labels [OPTIONS] REPOSITORY
    #
    # Listing labels of desired repository.
    #
    # Options:
    #   --help  Show this message and exit.
    invocation = invoker_norec('list_labels', '--help')

    assert invocation.result.exit_code == 0
    assert '--help' in invocation.result.output


def test_help_list_repos(invoker_norec):
    # There must be standard click help describing options
    # and commands (you should write description for each)
    # It should look like this:
    # Usage: labelord.py list_repos [OPTIONS]
    #
    # Listing accessible repositories.
    #
    # Options:
    #   --help Show this message and exit.
    invocation = invoker_norec('list_repos', '--help')

    assert invocation.result.exit_code == 0
    assert '--help' in invocation.result.output


def test_help_list_run(invoker_norec):
    # There must be standard click help describing options
    # and commands (you should write description for each)
    # It should look like this:
    # Usage: labelord.py run [OPTIONS] <update|replace>
    #
    # Run labels processing.
    #
    # Options:
    #   -t, --template-repo TEXT  Repository which serves as labels template.
    #   -d, --dry-run             Proceed with just dry run.
    #   -v, --verbose             Really exhaustive output.
    #   -q, --quiet               No output at all.
    #   -a, --all-repos           Run for all repositories available.
    #   --help                    Show this message and exit.
    invocation = invoker_norec('run', '--help')

    assert invocation.result.exit_code == 0
    assert '-t, --template-repo' in invocation.result.output
    assert '-d, --dry-run' in invocation.result.output
    assert '-v, --verbose' in invocation.result.output
    assert '-q, --quiet' in invocation.result.output
    assert '-a, --all-repos' in invocation.result.output
    assert '--help' in invocation.result.output


def test_version(invoker_norec):
    # There must be standard click version option
    # It should look like this:
    # labelord, version 0.1
    invocation = invoker_norec('--version')

    assert invocation.result.exit_code == 0
    assert 'labelord, version 0.1' in invocation.result.output


def test_precedence_template_repo(invoker, utils):
    # repo4 is empty and has higher precedence than repo3
    # in the config
    invocation = invoker('-c', utils.config('config_templaterepo'),
                         'run', 'update', '-t', 'MarekSuchanek/repo4',
                         session_expectations={
                             'get': 3,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'

