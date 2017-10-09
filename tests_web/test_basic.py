# Test all routes (send dummy request and receive OK response)
# These are without HTTP Basic Auth


def test_homepage(client_maker):
    # Test if app is able to respond to "GET /"
    client = client_maker('config_basic')
    result = client.get('/')
    assert result.status == '200 OK'


def test_webhook_ping(client_maker, utils):
    # Test if app is able to accept ping event signed with "S3cret!"
    client = client_maker('config_basic')
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_ping_webhook'),
        headers={
            'X-Hub-Signature': 'sha1=b7a7bacc401abde76ef575b2f3f436ae28aad8ec',
            'X-GitHub-Event': 'ping',
            'X-Github-Delivery': '64603d10-a3bb-11e7-82bc-0764f2d1a900',
            'X-Request-Id': 'e118e5e1-6763-4854-8b19-595c27b00135'
        }
    )
    assert result.status == '200 OK'
