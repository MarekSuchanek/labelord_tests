import sys, os
import betamax
import json
import pytest
import requests


ABS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = ABS_PATH + '/fixtures'
CASSETTES_PATH = FIXTURES_PATH + '/cassettes'
CONFIGS_PATH = FIXTURES_PATH + '/configs'
DATA_PATH = FIXTURES_PATH + '/data'

sys.path.insert(0, ABS_PATH + '/../')


def decode_if_bytes(obj, encoding='utf-8'):
    if isinstance(obj, bytes):
        return obj.decode(encoding)
    return obj


class GitHubMatcher(betamax.BaseMatcher):
    name = 'mipyt-github'

    @staticmethod
    def _has_correct_token(request):
        # GitHub token should be in headers (thisIsNotRealToken is used in tests)
        return request.headers.get('Authorization', '') == 'token thisIsNotRealToken'

    @staticmethod
    def _has_user_agent(request):
        # GitHub requires User-Agent, requests should do it automatically
        return request.headers.get('User-Agent', None) is not None

    @staticmethod
    def _match_body_json(request, recorded_request):
        if request.body is None:
            # Tested body is empty so should the recorded
            return recorded_request['body']['string'] == ''
        if recorded_request['body']['string'] == '':
            # Recorded body is empty but tested is not
            return False

        data1 = json.loads(recorded_request['body']['string'])
        data2 = json.loads(decode_if_bytes(request.body))
        # Compare JSON data from bodies
        return data1 == data2

    def match(self, request, recorded_request):
        return self._has_correct_token(request) and \
               self._has_user_agent(request) and \
               self._match_body_json(request, recorded_request)


betamax.Betamax.register_request_matcher(GitHubMatcher)

with betamax.Betamax.configure() as config:
    config.cassette_library_dir = CASSETTES_PATH
    config.default_cassette_options['match_requests_on'] = [
        'method',
        'uri',
        'mipyt-github'
    ]
    token = os.environ.get('GITHUB_TOKEN', '<TOKEN>')
    if 'GITHUB_TOKEN' in os.environ:
        config.default_cassette_options['record_mode'] = 'once'
    else:
        config.default_cassette_options['record_mode'] = 'none'
    config.define_cassette_placeholder('<TOKEN>', token)


class Utils:
    BETAMAX_ERRORS = 0

    @staticmethod
    def config(name):
        return CONFIGS_PATH + '/' + name + '.cfg'

    @staticmethod
    def load_data(name):
        with open(DATA_PATH + '/' + name + '.json') as f:
            return f.read()

    @staticmethod
    def create_auth(username, password):
        import base64
        return {
            'Authorization': 'Basic ' + base64.b64encode(
                bytes(username + ":" + password, 'ascii')
            ).decode('ascii')
        }

    @classmethod
    def monkeypatch_betamaxerror(cls, monkeypatch):
        cls.BETAMAX_ERRORS = 0
        def monkey_init(self, message):
            super(betamax.BetamaxError, self).__init__(message)
            cls.BETAMAX_ERRORS += 1

        monkeypatch.setattr(betamax.BetamaxError, '__init__', monkey_init)


@pytest.fixture
def utils():
    return Utils()


class LabelordInvocation:

    def __init__(self, runner, result, session):
        self.runner = runner
        self.result = result
        self.session = session


@pytest.fixture
def invoker(betamax_session):
    from click.testing import CliRunner
    from flexmock import flexmock
    from labelord import cli

    def invoker_inner(*args, isolated=False, session_expectations=None):
        session_mock = flexmock(betamax_session or requests.Session())
        if session_expectations is not None:
            for what, count in session_expectations.items():
                session_mock.should_call(what).times(count)
        runner = CliRunner()
        args = [a for a in args if a is not None]
        if isolated:
            with runner.isolated_filesystem():
                result = runner.invoke(cli, args,
                                       obj={'session': session_mock})
        else:
            result = runner.invoke(cli, args,
                                   obj={'session': session_mock})
        return LabelordInvocation(runner, result, session_mock)
    return invoker_inner


@pytest.fixture
def invoker_norec():
    return invoker(None)


@pytest.fixture
def client_maker(betamax_session, utils, monkeypatch):
    def inner_maker(config, own_config_path=False,
                    session_expectations=None):
        from flexmock import flexmock

        if not own_config_path:
            config = Utils.config(config)

        session_mock = flexmock(betamax_session or requests.Session())

        # MonkeyPatch BetamaxError
        utils.monkeypatch_betamaxerror(monkeypatch)

        if os.environ.get('LABELORD_SESSION_SPY', '').lower() != 'off' and \
           session_expectations is not None:
            for what, count in session_expectations.items():
                session_mock.should_call(what).times(count)

        os.environ['LABELORD_CONFIG'] = config
        from labelord import app
        app.inject_session(betamax_session)
        app.reload_config()
        client = app.test_client()
        return client
    yield inner_maker

    # Check number of created BetamaxErrors
    # You should catch only your/specific exceptions
    try:
        assert utils.BETAMAX_ERRORS == 0, \
            'There were some BetamaxErrors (although you might ' \
            'have caught them)!'
    finally:
        Utils.BETAMAX_ERRORS = 0
