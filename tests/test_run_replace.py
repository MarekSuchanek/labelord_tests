# All tests here use this:
# repo1 = [(label1, FFAA00), (label3, 00FF33), (label4, 771077)]
# repo2 = [(label2, CCAAFF)]
# repo3 = [(label4, 666666), (label5, C0B011)]
# repo4 = []


def test_replace_empty_repos(invoker, utils):
    # GET: 0
    # POST: 0
    # PATCH: 0
    # DELETE: 0
    invocation = invoker('-c', utils.config('config_emptyrepos'),
                         'run', 'replace',
                         session_expectations={
                             'get': 0,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 0 repo(s) updated successfully'


def test_replace_empty_labels(invoker, utils):
    # GET: 2 (repo1: 1, repo2: 1)
    # POST: 0
    # PATCH: 0
    # DELETE: 4 (repo1: 3, repo2: 1)
    invocation = invoker('--config', utils.config('config_emptylabels'),
                         'run', 'replace',
                         session_expectations={
                             'get': 2,
                             'post': 0,
                             'patch': 0,
                             'delete': 4
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'


def test_replace_normal(invoker, utils):
    # GET: 2 (repo1: 1, repo2: 1)
    # POST: 3 (repo1: 1, repo2: 2)
    # PATCH: 1 (repo1: 1, repo2: 0)
    # DELETE: 1 (repo1: 1, repo2: 0)
    invocation = invoker('-c', utils.config('config_normal'),
                         'run', 'replace',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'


def test_replace_all_repos(invoker, utils):
    # GET: 5 (all: 1, repo1: 1, repo2: 1, repo3: 1, repo4: 1)
    # POST: 9 (repo1: 1, repo2: 2, repo3: 3, repo4: 3)
    # PATCH: 1 (repo1: 1, repo2: 0, repo3: 0, repo4: 0)
    # DELETE: 3 (repo1: 1, repo2: 0, repo3: 2, repo4: 0)
    invocation = invoker('--config', utils.config('config_normal'),
                         'run', 'replace', '--all-repos',
                         session_expectations={
                             'get': 5,
                             'post': 9,
                             'patch': 1,
                             'delete': 3
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 4 repo(s) updated successfully'


def test_replace_template_repo(invoker, utils):
    # GET: 3 (repo1: 1, repo2: 1, repo3: 1)
    # POST: 3 (repo1: 1, repo2: 2)
    # PATCH: 1 (repo1: 1, repo2: 0)
    # DELETE: 3 (repo1: 2, repo2: 1)
    invocation = invoker('-c', utils.config('config_templaterepo'),
                         'run', 'replace',
                         session_expectations={
                             'get': 3,
                             'post': 3,
                             'patch': 1,
                             'delete': 3
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'


def test_replace_with_errors(invoker, utils):
    # GET: 3 (repo1: 1, repo2: 1, repo7: 1)
    # POST: 5 (repo1: 2, repo2: 3)
    # PATCH: 1 (repo1: 1, repo2: 0)
    # DELETE: 1 (repo1: 1, repo2: 0)
    invocation = invoker('--config', utils.config('config_errors'),
                         'run', 'replace',
                         session_expectations={
                             'get': 3,
                             'post': 5,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 7 and lines[-1] == ''
    assert 'ERROR: UPD; MarekSuchanek/repo1; label3; 00FFXX; 422 - Validation Failed' in lines
    assert 'ERROR: ADD; MarekSuchanek/repo2; label3; 00FFXX; 422 - Validation Failed' in lines
    assert 'ERROR: ADD; MarekSuchanek/repo1; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert 'ERROR: ADD; MarekSuchanek/repo2; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert 'ERROR: LBL; MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == 'SUMMARY: 5 error(s) in total, please check log above'


def test_replace_dry(invoker, utils):
    # GET: 2 (repo1: 1, repo2: 1)
    # POST: 0 (dry run)
    # PATCH: 0 (dry run)
    # DELETE: 0 (dry run)
    invocation = invoker('--config', utils.config('config_normal'),
                         'run', 'replace', '--dry-run',
                         session_expectations={
                             'get': 2,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'


def test_replace_dry_with_errors(invoker, utils):
    # GET: 3 (repo1: 1, repo2: 1, repo7: 1)
    # POST: 0 (dry run)
    # PATCH: 0 (dry run)
    # DELETE: 0 (dry run)
    invocation = invoker('-c', utils.config('config_errors'),
                         'run', 'replace', '-d',
                         session_expectations={
                             'get': 3,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 3 and lines[-1] == ''
    assert 'ERROR: LBL; MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == 'SUMMARY: 1 error(s) in total, please check log above'
    