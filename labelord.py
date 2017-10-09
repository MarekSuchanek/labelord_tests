# This is skeleton for labelord module
# MI-PYT, task 1 (requests+click)
# File: labelord.py
# TODO: create requirements.txt and install
import click
import flask
import os
import requests

# Structure your implementation as you want (OOP, FP, ...)
# Try to make it DRY also for your own good


@click.group('labelord')
@click.pass_context
def cli(ctx):
    # TODO: Add and process required app-wide options
    # You can/should use context 'ctx' for passing
    # data and objects to commands

    # Use this session for communication with GitHub
    session = ctx.obj.get('session', requests.Session())


@cli.command()
@click.pass_context
def list_repos(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'list_repos' command
    ...


@cli.command()
@click.pass_context
def list_labels(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'list_labels' command
    ...


@cli.command()
@click.pass_context
def run(ctx):
    # TODO: Add required options/arguments
    # TODO: Implement the 'run' command
    ...

#####################################################################
# STARING NEW FLASK SKELETON (Task 2 - flask)


class LabelordWeb(flask.Flask):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # You can do something here, but you don't have to...
        # Adding more args before *args is also possible
        # You need to pass import_name to super as first arg or
        # via keyword (e.g. import_name=__name__)
        # Be careful not to override something Flask-specific
        # @see http://flask.pocoo.org/docs/0.12/api/
        # @see https://github.com/pallets/flask

    def inject_session(self, session):
        # TODO: inject session for communication with GitHub
        # The tests will call this method to pass the testing session.
        # Always use session from this call (it will be called before
        # any HTTP request). If this method is not called, create new
        # session.
        ...

    def reload_config(self):
        # TODO: check envvar LABELORD_CONFIG and reload the config
        # Because there are problems with reimporting the app with
        # different configuration, this method will be called in
        # order to reload configuration file. Check if everything
        # is correctly set-up
        ...


# TODO: instantiate LabelordWeb app
# Be careful with configs, this is module-wide variable,
# you want to be able to run CLI app as it was in task 1.
app = ...

# TODO: implement web app
# hint: you can use flask.current_app (inside app context)


@cli.command()
@click.pass_context
def run_server(ctx):
    # TODO: implement the command for starting web app (use app.run)
    # Don't forget to app the session from context to app
    ...


# ENDING  NEW FLASK SKELETON
#####################################################################

if __name__ == '__main__':
    cli(obj={})
