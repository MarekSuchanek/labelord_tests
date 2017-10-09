# All tests here use this:
# repo1 = [(label1, FFAA00), (label3, 00FF33), (label4, 771077)]
# repo2 = [(label2, CCAAFF)]
# repo3 = [(label4, 666666), (label5, C0B011)]
# repo4 = []


def test_update_verbose(invoker, utils):
    invocation = invoker('--config', utils.config('config_normal'),
                         'run', 'update', '--verbose',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 6 and lines[-1] == ''
    assert '[ADD][SUC] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[UPD][SUC] MarekSuchanek/repo1; label3; 00FF00' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label3; 00FF00' in lines
    assert lines[-2] == '[SUMMARY] 2 repo(s) updated successfully'


def test_replace_verbose(invoker, utils):
    invocation = invoker('-c', utils.config('config_normal'),
                         'run', 'replace', '-v',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 7 and lines[-1] == ''
    assert '[ADD][SUC] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[UPD][SUC] MarekSuchanek/repo1; label3; 00FF00' in lines
    assert '[DEL][SUC] MarekSuchanek/repo1; label4; 771077' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label3; 00FF00' in lines
    assert lines[-2] == '[SUMMARY] 2 repo(s) updated successfully'


def test_update_normal(invoker, utils):
    invocation = invoker('--config', utils.config('config_normal'),
                         'run', 'update', '--quiet', '--verbose',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 2 and lines[-1] == ''
    assert lines[0] == 'SUMMARY: 2 repo(s) updated successfully'


def test_replace_normal(invoker, utils):
    invocation = invoker('-c', utils.config('config_normal'),
                         'run', 'replace', '-q', '-v',
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


def test_update_quiet(invoker, utils):
    invocation = invoker('-c', utils.config('config_normal'),
                         'run', 'update', '-q',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 1 and lines[-1] == ''


def test_replace_quiet(invoker, utils):
    invocation = invoker('--config', utils.config('config_normal'),
                         'run', 'replace', '--quiet',
                         session_expectations={
                             'get': 2,
                             'post': 3,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 0
    assert len(lines) == 1 and lines[-1] == ''


def test_update_verbose_with_errors(invoker, utils):
    invocation = invoker('-c', utils.config('config_errors'),
                         'run', 'update', '-v',
                         session_expectations={
                             'get': 3,
                             'post': 5,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 9 and lines[-1] == ''
    assert '[ADD][SUC] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[ADD][ERR] MarekSuchanek/repo1; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert '[UPD][ERR] MarekSuchanek/repo1; label3; 00FFXX; 422 - Validation Failed' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][ERR] MarekSuchanek/repo2; label3; 00FFXX; 422 - Validation Failed' in lines
    assert '[ADD][ERR] MarekSuchanek/repo2; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert '[LBL][ERR] MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == '[SUMMARY] 5 error(s) in total, please check log above'


def test_replace_verbose_with_errors(invoker, utils):
    invocation = invoker('--config', utils.config('config_errors'),
                         'run', 'replace', '--verbose',
                         session_expectations={
                             'get': 3,
                             'post': 5,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 10 and lines[-1] == ''
    assert '[ADD][SUC] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[ADD][ERR] MarekSuchanek/repo1; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert '[UPD][ERR] MarekSuchanek/repo1; label3; 00FFXX; 422 - Validation Failed' in lines
    assert '[DEL][SUC] MarekSuchanek/repo1; label4; 771077' in lines
    assert '[ADD][SUC] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][ERR] MarekSuchanek/repo2; label3; 00FFXX; 422 - Validation Failed' in lines
    assert '[ADD][ERR] MarekSuchanek/repo2; label7; 00FFCCAA; 422 - Validation Failed' in lines
    assert '[LBL][ERR] MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == '[SUMMARY] 5 error(s) in total, please check log above'


def test_update_quiet_with_errors(invoker, utils):
    invocation = invoker('-c', utils.config('config_errors'),
                         'run', 'update', '-q',
                         session_expectations={
                             'get': 3,
                             'post': 5,
                             'patch': 1,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 1 and lines[-1] == ''


def test_replace_quiet_with_errors(invoker, utils):
    invocation = invoker('--config', utils.config('config_errors'),
                         'run', 'replace', '--quiet',
                         session_expectations={
                             'get': 3,
                             'post': 5,
                             'patch': 1,
                             'delete': 1
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 1 and lines[-1] == ''


def test_update_dry_verbose_with_errors(invoker, utils):
    invocation = invoker('-c', utils.config('config_errors'),
                         'run', 'update', '-v', '-d',
                         session_expectations={
                             'get': 3,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 9 and lines[-1] == ''
    assert '[ADD][DRY] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[ADD][DRY] MarekSuchanek/repo1; label7; 00FFCCAA' in lines
    assert '[UPD][DRY] MarekSuchanek/repo1; label3; 00FFXX' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label3; 00FFXX' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label7; 00FFCCAA' in lines
    assert '[LBL][ERR] MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == '[SUMMARY] 1 error(s) in total, please check log above'


def test_replace_dry_verbose_with_errors(invoker, utils):
    invocation = invoker('--config', utils.config('config_errors'),
                         'run', 'replace', '--verbose', '--dry-run',
                         session_expectations={
                             'get': 3,
                             'post': 0,
                             'patch': 0,
                             'delete': 0
                         })
    lines = invocation.result.output.split('\n')

    assert invocation.result.exit_code == 10
    assert len(lines) == 10 and lines[-1] == ''
    assert '[ADD][DRY] MarekSuchanek/repo1; label2; CCAAFF' in lines
    assert '[ADD][DRY] MarekSuchanek/repo1; label7; 00FFCCAA' in lines
    assert '[UPD][DRY] MarekSuchanek/repo1; label3; 00FFXX' in lines
    assert '[DEL][DRY] MarekSuchanek/repo1; label4; 771077' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label1; FFAA00' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label3; 00FFXX' in lines
    assert '[ADD][DRY] MarekSuchanek/repo2; label7; 00FFCCAA' in lines
    assert '[LBL][ERR] MarekSuchanek/repo7; 404 - Not Found' in lines
    assert lines[-2] == '[SUMMARY] 1 error(s) in total, please check log above'
