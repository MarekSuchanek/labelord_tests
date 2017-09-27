# This is skeleton for labelord module
# MI-PYT, task 1 (requests+click)
# File: labelord.py
# TODO: create requirements.txt and install
import click
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


if __name__ == '__main__':
    cli(obj={})
