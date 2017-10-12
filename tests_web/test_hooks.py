

def test_ping(client_maker, utils):
    # Test if app is able to accept ping event signed with "S3cret!"
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 0, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_ping_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=b7a7bacc401abde76ef575b2f3f436ae28aad8ec',
            'X-GitHub-Event': 'ping',
            'X-Github-Delivery': '64603d10-a3bb-11e7-82bc-0764f2d1a900',
            'X-Request-Id': 'e118e5e1-6763-4854-8b19-595c27b00135'
        }
    )
    assert result.status == '200 OK'


def test_label_created(client_maker, utils):
    # Test if app is able to accept and process label webhook with
    # created event (replication is being checked!)
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 1, 'delete': 0, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_label_created_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=5928ae03413a3b693b9cb0cbc8746921a1c55bae',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'bf64f0d0-a536-11e7-8d70-e656edf279e1',
            'X-Request-Id': '55eedbbd-6794-4273-9438-af5a69cb24c1'
        }
    )
    assert result.status == '200 OK'


def test_label_edited(client_maker, utils):
    # Test if app is able to accept and process label webhook with
    # edited event (replication is being checked!)
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 0, 'patch': 1
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_label_edited_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=14ddf55c89d68663c4faaa2d40166fbf65147469',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '5379b940-a537-11e7-986d-e4063d6efb49',
            'X-Request-Id': '788dcf62-e4d9-47c7-a7a8-3e9ea4f515d8'
        }
    )
    assert result.status == '200 OK'


def test_label_deleted(client_maker, utils):
    # Test if app is able to accept and process label webhook with
    # deleted action (replication is being checked!)
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 1, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_label_deleted_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=e0b2a06fbf02b113bafaca8030c40ce90c61aa0d',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'ca26252e-a537-11e7-9bc9-062206b3cfa7',
            'X-Request-Id': '328edc78-a931-4e15-94b0-a971e98dceb7'
        }
    )
    assert result.status == '200 OK'


def test_label_created_not_allowed(client_maker, utils):
    # Test if app wont process webhook from not allowed repository
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 0, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('labelord_label_created_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=079a544672bb68c8c6510b94f151784f49a6fe5e',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '8f63ad50-a53a-11e7-86ff-d2dc5471be65',
            'X-Request-Id': '37395d17-283b-421d-ae41-d1817c6424f4'
        }
    )
    assert result.status == '400 BAD REQUEST'


def test_no_signature(client_maker, utils):
    # Test if app wont process webhook without signature header
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 0, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_label_created_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'bf64f0d0-a536-11e7-8d70-e656edf279e1',
            'X-Request-Id': '55eedbbd-6794-4273-9438-af5a69cb24c1'
        }
    )
    assert result.status == '401 UNAUTHORIZED'


def test_bad_signature(client_maker, utils):
    # Test if app wont process webhook with incorrect signature
    client = client_maker('config_basic', session_expectations={
        'get': 0, 'post': 0, 'delete': 0, 'patch': 0
    })
    result = client.post(
        '/',
        data=utils.load_data('pyplayground_label_created_webhook'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=b7a7bacc401abde7aaaaabb2f3f436ae28aad8ec',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'bf64f0d0-a536-11e7-8d70-e656edf279e1',
            'X-Request-Id': '55eedbbd-6794-4273-9438-af5a69cb24c1'
        }
    )
    assert result.status == '401 UNAUTHORIZED'


def test_no_redundant(client_maker, utils):
    import time
    client = client_maker('config_3repos', session_expectations={
        'get': 0, 'post': 2, 'delete': 2, 'patch': 2
    })
    # Label 'Security' (#FF3300) has been created in 'MarekSuchanek/pyplayground'
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_pyplayground_created'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=4f8741adb2fc715621dc50ecb4a68e2eb5ef1388',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '282a9470-a5f1-11e7-9c32-ec4899ee1f9d',
            'X-Request-Id': '9f1ed96d-9979-4328-a679-464f3f4d3ac5'
        }
    )
    assert result.status == '200 OK'
    # Weird - no webhooks are sent when labels created like this (30-09-2017)
    # Probably it should - better to treat it in your app just as edited
    # and deleted events, where it happens!

    time.sleep(0.5)
    # Label 'Security' has been edited (#FF6600) in 'MarekSuchanek/repocribro'
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_repocribro_edited'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=eae291659e007d65f47f6b6d86c3a3911b2801a9',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'b8000580-a5f1-11e7-80d8-36c9c46eb7dc',
            'X-Request-Id': '0f15c5c9-670f-43ac-8406-8fb8c9825ecd'
        }
    )
    assert result.status == '200 OK'
    # After editing new two webhooks incoming
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_pyplayground_edited'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=ea8800cbc0fe042e35f3a2ba9a2709735e161d84',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'f6e8c200-a5f1-11e7-921d-f299305b80f5',
            'X-Request-Id': '6fe71645-c177-405e-8f87-444261fa3be6'
        }
    )
    assert result.status == '200 OK'
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_maze_edited'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=24f416b05588780e9fb001062ca09e17496c53d6',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': 'f70ac8f0-a5f1-11e7-8e49-c14ae979dc4a',
            'X-Request-Id': '9a806fcd-223e-4676-b830-312adabb1ebe'
        }
    )
    assert result.status == '200 OK'

    time.sleep(0.5)
    # Label 'Security' has been deleted in 'MarekSuchanek/maze'
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_maze_deleted'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=c9b996d5e5f6377358720173400187c0982fd181',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '78a6175c-a5f2-11e7-8a1e-f91095cb4f25',
            'X-Request-Id': '19cc9781-ed1f-4ab8-b308-f2b9ac178fac'
        }
    )
    assert result.status == '200 OK'
    # After deleting new two webhooks incoming
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_pyplayground_deleted'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=2cbd35c4571efe5a0e5cfe970b0c0ceda82109df',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '5a5e3d0a-a5f3-11e7-97cc-8b5c786576e9',
            'X-Request-Id': '8e85e90e-7764-4563-903a-35314b428dc4'
        }
    )
    assert result.status == '200 OK'
    result = client.post(
        '/',
        data=utils.load_data('no_redundant_repocribro_deleted'),
        headers={
            'Content-Type': 'application/json',
            'User-Agent': 'GitHub-Hookshot/e9907f9',
            'X-Hub-Signature': 'sha1=63ceb9cbafd69f3d2d2355f9d353dda25c4d93c7',
            'X-GitHub-Event': 'label',
            'X-Github-Delivery': '5a82019a-a5f3-11e7-8fe3-e2f56706bade',
            'X-Request-Id': '9210e34f-8cd9-4e0f-b1f5-5a7d543775ed'
        }
    )
    assert result.status == '200 OK'

