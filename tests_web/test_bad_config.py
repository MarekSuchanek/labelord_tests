import pytest


def test_no_repos(client_maker, capsys):
    # Test exit code and message for config without repos
    with pytest.raises(SystemExit) as info:
        client = client_maker('config_norepos')
        client.get('/')
    assert info.value.code == 7
    out, err = capsys.readouterr()
    assert '' in out
    assert 'No repositories specification has been found' in err


def test_no_labels(client_maker):
    # Ha! This is not a bad config at all...
    client = client_maker('config_nolabels')
    result = client.get('/')
    assert result.status == '200 OK'


def test_no_token(client_maker, capsys):
    # Test exit code and message for config without GitHub token
    with pytest.raises(SystemExit) as info:
        client = client_maker('config_notoken')
        client.get('/')
    assert info.value.code == 3
    out, err = capsys.readouterr()
    assert '' in out
    assert 'No GitHub token has been provided' in err


def test_no_webhook_secret(client_maker, capsys):
    # Test exit code and message for config without webhook secret
    with pytest.raises(SystemExit) as info:
        client = client_maker('config_nosecret')
        client.get('/')
    assert info.value.code == 8
    out, err = capsys.readouterr()
    assert '' in out
    assert 'No webhook secret has been provided' in err
