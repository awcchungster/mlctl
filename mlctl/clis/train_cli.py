import click
import os
from distutils.core import run_setup

from mlctl.clis.common.utils import determine_infra_plugin_from_job, parse_train_yamls, docker_instructions

@click.group(name='train', help="Train commands")
def train():
    pass

import sys
import time
@train.command(name="build", help="build a container for training")
def start():
    click.echo("Building container for training job")

    # TODO: make this a dynamic lookup
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    
    process = subprocess.Popen(['python3', './setup.py', 'train', '-t', 'train-image'],stdout=subprocess.PIPE)
    while True:
        output = process.stdout.readline()
        if process.poll() is not None:
            break
        if output:
            print (output.strip().decode())
    retval = process.poll()
    return

@train.command(name="push", help="push a container for training")
def start():

    # TODO:
    # Remove placeholder
    # check a state file for the container repo
    # tag the local image to the remote
    # push to the right repo
    click.echo("Pushing container for training job")
    def spinning_cursor():
        while True:
            for cursor in '|/-\\':
                yield cursor

    spinner = spinning_cursor()
    for _ in range(50):
        sys.stdout.write(next(spinner))
        sys.stdout.flush()
        time.sleep(0.1)
        sys.stdout.write('\b')
    

@train.command(name="build", help="build a container for train")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for train job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def build(provider_config, config, tag):
    

    job = parse_train_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['train']['name']

    # validate if there is a setup file to build from
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    click.echo("Building container for train job")
    
    # validate if there is a tag name, else use the default
    if tag:
        image_name = tag
    else:
        image_name = 'train-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','train',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(docker_instructions(image_name))
    return

@train.command(name="build", help="build a container for train")
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for train job", metavar='')
@click.option('--tag', '-t', help="Docker Image tag to save image to", metavar='')
def build(provider_config, config, tag):
    

    job = parse_train_yamls(config, provider_config)
    infrastructure_name = job.serialize()['infrastructure']['train']['name']

    # validate if there is a setup file to build from
    if not os.path.isfile('./setup.py'):
        print('Missing mlctl setup.py for building a mlctl universal container. \
        Try mlctl init, or navigating to the home directory of the project.')
        return
    click.echo("Building container for train job")
    
    # validate if there is a tag name, else use the default
    if tag:
        image_name = tag
    else:
        image_name = 'train-image'
    build = run_setup('./setup.py', 
        script_args=['sdist', '--dist-dir', './.mlctl','train',
        '-t', image_name,  '-p', infrastructure_name])
    click.echo(docker_instructions(image_name))
    return

@train.command(name="start", help="Train a model")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--config', '-c', required=True, help="config file containing parameters for train job", metavar='')
def start(profile, provider_config, config):
    job = parse_train_yamls(config, provider_config)
    train = determine_infra_plugin_from_job(job, profile)
    click.echo(train.start_train(
        job))


@train.command(name="info", help="Get train job information")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--config', '-c', required=False, help="name of train job", metavar='')
@click.option('--provider_config', '-p', envvar='PROVIDER_CONFIG', help="file location for the provider.yaml", metavar='')
@click.option('--name', '-n', required=False, help="name of train job", metavar='')
def info(profile, config, provider_config, name):
    job = parse_train_yamls(config, provider_config)
    train = determine_infra_plugin_from_job(job, profile)
    if name:
        job.update_name(name)
    click.echo(train.get_train_info(
        job))


@train.command(name="stop", help="Stop a train job")
@click.option('--profile', '-pr', envvar='PROFILE', help="credentials profile or file location", metavar='')
@click.option('--train-job-name', '-t', required=True, help="name of train job", metavar='')
@click.option('--config', '-c', required=False, help="name of train job", metavar='')
def stop(profile, plugin, train_job_name, hyperparameter_tuning):
    train = determine_plugin(plugin, profile, 'train')

    click.echo(train.stop_train(
        train_job_name, hyperparameter_tuning))
