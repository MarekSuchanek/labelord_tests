

def test_app_info(client_maker):
    # Test if index describes the application
    client = client_maker('config_basic')
    result = client.get('/')
    assert result.status == '200 OK'
    page = result.data.decode('utf-8')
    assert 'labelord' in page.lower()
    assert 'master-to-master' in page
    assert 'webhook' in page
    assert 'GitHub' in page


def test_repos_list(client_maker):
    # Test if app lists repos from config file
    client = client_maker('config_basic')
    result = client.get('/')
    assert result.status == '200 OK'
    page = result.data.decode('utf-8')
    assert 'MarekSuchanek/pyplayground' in page
    assert 'MarekSuchanek/repocribro' in page
    assert 'MarekSuchanek/labelord' not in page


def test_repos_list_other(client_maker):
    # Test if app lists repos from different config file
    client = client_maker('config_3repos')
    result = client.get('/')
    assert result.status == '200 OK'
    page = result.data.decode('utf-8')
    assert 'MarekSuchanek/pyplayground' in page
    assert 'MarekSuchanek/repocribro' in page
    assert 'MarekSuchanek/labelord' not in page
    assert 'MarekSuchanek/maze' in page


def test_repos_links(client_maker):
    # Test if app lists repos from config file with links
    client = client_maker('config_basic')
    result = client.get('/')
    assert result.status == '200 OK'
    page = result.data.decode('utf-8')

    def gh_link(reposlug):
        return 'https://github.com/' + reposlug

    assert gh_link('MarekSuchanek/pyplayground') in page
    assert gh_link('MarekSuchanek/repocribro') in page
    assert gh_link('MarekSuchanek/labelord') not in page
