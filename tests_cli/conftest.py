import sys, os
import betamax
import json
import pytest
import requests


ABS_PATH = os.path.abspath(os.path.dirname(__file__))
FIXTURES_PATH = ABS_PATH + '/fixtures'
CASSETTES_PATH = FIXTURES_PATH + '/cassettes'
CONFIGS_PATH = FIXTURES_PATH + '/configs'

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

    @staticmethod
    def config(name):
        return CONFIGS_PATH + '/' + name + '.cfg'


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
        if os.environ.get('LABELORD_SESSION_SPY', '').lower() != 'off' and \
           session_expectations is not None:
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
