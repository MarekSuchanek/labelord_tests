import json
import click

REPO_JSON = '{\"issues_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/issues{/number}\", \"deployments_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/deployments\", \"stargazers_count\": 83, \"forks_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/forks\", \"mirror_url\": null, \"subscription_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/subscription\", \"notifications_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/notifications{?since,all,participating}\", \"collaborators_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/collaborators{/collaborator}\", \"updated_at\": \"2017-08-27T20:49:41Z\", \"private\": false, \"pulls_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/pulls{/number}\", \"issue_comment_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/issues/comments{/number}\", \"labels_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/labels{/name}\", \"has_wiki\": true, \"full_name\": \"MarekSuchanek/repoXXX\", \"owner\": {\"following_url\": \"https://api.github.com/users/cvut/following{/other_user}\", \"events_url\": \"https://api.github.com/users/cvut/events{/privacy}\", \"organizations_url\": \"https://api.github.com/users/cvut/orgs\", \"url\": \"https://api.github.com/users/cvut\", \"gists_url\": \"https://api.github.com/users/cvut/gists{/gist_id}\", \"html_url\": \"https://github.com/cvut\", \"subscriptions_url\": \"https://api.github.com/users/cvut/subscriptions\", \"avatar_url\": \"https://avatars3.githubusercontent.com/u/2183308?v=4\", \"repos_url\": \"https://api.github.com/users/cvut/repos\", \"received_events_url\": \"https://api.github.com/users/cvut/received_events\", \"gravatar_id\": \"\", \"starred_url\": \"https://api.github.com/users/cvut/starred{/owner}{/repo}\", \"site_admin\": false, \"login\": \"cvut\", \"type\": \"Organization\", \"id\": 2183308, \"followers_url\": \"https://api.github.com/users/cvut/followers\"}, \"statuses_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/statuses/{sha}\", \"id\": 58668ZZZ, \"keys_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/keys{/key_id}\", \"description\": \"Materi\\u00e1ly k p\\u0159edm\\u011btu MI-PYT na FIT \\u010cVUT\", \"tags_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/tags\", \"downloads_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/downloads\", \"assignees_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/assignees{/user}\", \"contents_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/contents/{+path}\", \"has_pages\": false, \"git_refs_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/git/refs{/sha}\", \"open_issues_count\": 10, \"has_projects\": true, \"clone_url\": \"https://github.com/MarekSuchanek/repoXXX.git\", \"watchers_count\": 83, \"git_tags_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/git/tags{/sha}\", \"milestones_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/milestones{/number}\", \"languages_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/languages\", \"size\": 4058, \"homepage\": \"https://edux.fit.cvut.cz/courses/MI-PYT/\", \"fork\": false, \"commits_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/commits{/sha}\", \"releases_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/releases{/id}\", \"issue_events_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/issues/events{/number}\", \"archive_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/{archive_format}{/ref}\", \"comments_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/comments{/number}\", \"events_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/events\", \"contributors_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/contributors\", \"html_url\": \"https://github.com/MarekSuchanek/repoXXX\", \"forks\": 20, \"compare_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/compare/{base}...{head}\", \"open_issues\": 10, \"git_url\": \"git://github.com/MarekSuchanek/repoXXX.git\", \"svn_url\": \"https://github.com/MarekSuchanek/repoXXX\", \"merges_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/merges\", \"has_issues\": true, \"ssh_url\": \"git@github.com:MarekSuchanek/repoXXX.git\", \"blobs_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/git/blobs{/sha}\", \"git_commits_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/git/commits{/sha}\", \"hooks_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/hooks\", \"has_downloads\": true, \"watchers\": 83, \"name\": \"MI-PYT\", \"language\": \"Jupyter Notebook\", \"url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX\", \"created_at\": \"2016-05-12T18:57:56Z\", \"pushed_at\": \"2017-09-14T10:37:11Z\", \"forks_count\": 20, \"default_branch\": \"master\", \"teams_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/teams\", \"trees_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/git/trees{/sha}\", \"branches_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/branches{/branch}\", \"subscribers_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/subscribers\", \"permissions\": {\"admin\": false, \"push\": true, \"pull\": true}, \"stargazers_url\": \"https://api.github.com/repos/MarekSuchanek/repoXXX/stargazers\"}'
LABEL_JSON = '{\"id\": 493652ZZZ, \"url\": \"https://api.github.com/repos/MarekSuchanek/repo1/labels/labelXXX\", \"name\": \"labelXXX\", \"color\": \"ABCZZZ\", \"default\": true}'


@click.group()
def cli():
    pass


@cli.command()
@click.argument('text_file', type=click.File('r'))
def string2json(text_file):
    data = json.loads(json.load(text_file))
    click.echo(json.dumps(data, indent=2, sort_keys=False))


@cli.command()
@click.argument('json_file', type=click.File('r'))
def json2string(json_file):
    data = json.load(json_file)
    click.echo(json.dumps(json.dumps(data)))


@cli.command()
@click.argument('start', type=click.INT)
@click.argument('end', type=click.INT)
def generate_repos(start, end):
    data = []
    for i in range(start, end):
        string = REPO_JSON.replace('repoXXX', 'repo{}'.format(i))
        string = string.replace('ZZZ', '{}'.format(i+100))
        data.append(json.loads(string))
    click.echo(json.dumps(data, indent=2, sort_keys=False))


@cli.command()
@click.argument('start', type=click.INT)
@click.argument('end', type=click.INT)
def generate_labels(start, end):
    data = []
    for i in range(start, end):
        string = LABEL_JSON.replace('labelXXX', 'label{}'.format(i))
        string = string.replace('ZZZ', '{}'.format(i+100))
        data.append(json.loads(string))
    click.echo(json.dumps(data, indent=2, sort_keys=False))


if __name__ == '__main__':
    cli()
