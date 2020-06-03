#!/usr/bin/env python3
"""
Created on June 03 2020

@author: Joan Hérisson
@description: Galaxy script to query rpCompletion service

"""
from sys import path as sys_path
sys_path.insert(0, '/home/src')
from main import build_parser as tool_buildparser
from main import entrypoint as tool_entrypoint
from tarfile import open as tarfile_open
from tarfile import TarInfo as tarfile_TarInfo
from tempfile import TemporaryDirectory as tempfile_tempdir
from os import listdir as os_listdir



if __name__ == "__main__":

    # Parse arguments with the tool parser
    parser = tool_buildparser()
    params = parser.parse_args()

    # Process in a temporary folder that will be automatically removed after exit
    with tempfile_tempdir() as tmpdirname:

        # Prepare arguments for the tool
        args = [
            '-rules_type', params.rules_type,
            '-output', params.output,
            '-diameters', params.diameters
            ]

        # Run the tool
        tool_entrypoint(args)

        # Format ouput data as expected by the wrapper
        with tarfile_open(params.output, mode='w:gz') as tf:
            for name in os_listdir(tmpdirname):
                tf.add(tmpdirname+"/"+name, arcname=name)










#!/usr/bin/env python3
"""
Created on September 21 2019

@author: Melchior du Lac
@description: Extract the sink from an SBML into RP2 friendly format

"""
import argparse
import tempfile
import os
import logging
import shutil
import docker


##
#
#
def main(output, output_format='tar', rule_type='retro', diameters='2,4,6,8,10,12,14,16'):
    docker_client = docker.from_env()
    image_str = 'brsynth/retrorules-standalone'
    try:
        image = docker_client.images.get(image_str)
    except docker.errors.ImageNotFound:
        logging.warning('Could not find the image, trying to pull it')
        try:
            docker_client.images.pull(image_str)
            image = docker_client.images.get(image_str)
        except docker.errors.ImageNotFound:
            logging.error('Cannot pull image: '+str(image_str))
            exit(1)
    #create a temporary folder to make the connection between the
    #docker and the local files
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        command = ['/home/tool_RetroRules.py',
                   '-rule_type',
                   rule_type,
                   '-diameters',
                   diameters,
                   '-output_format',
                   output_format,
                   '-output',
                   '/home/tmp_output/output.dat']
        container = docker_client.containers.run(image_str,
                                                 command,
                                                 detach=True,
                                                 stderr=True,
                                                 volumes={tmpOutputFolder+'/': {'bind': '/home/tmp_output', 'mode': 'rw'}})
        container.wait()
        err = container.logs(stdout=False, stderr=True)
        err_str = err.decode('utf-8')
        print(err_str)
        if not 'ERROR' in err_str:
            shutil.copy(tmpOutputFolder+'/output.dat', output)
        container.remove()


from sys import argv as sys_argv
from argparse import ArgumentParser as argparse_ArgumentParser
from os import path as os_path
from os import mkdir as os_mkdir

from sys import path as sys_path
sys_path.insert(0, '/home/rpCache')
from rpCache import rpCache
from rpCache import add_arguments as rpCache_add_arguments
from rpCompletion import rpCompletion

def add_arguments(parser):
    parser.add_argument('-rule_type', type=str)
    parser.add_argument('-output', type=str)
    parser.add_argument('-diameters', type=str, default='2,4,6,8,10,12,14,16')
    parser.add_argument('-output_format', type=str)
    return parser

def build_parser():
    parser = argparse_ArgumentParser('Python wrapper to generate RetroRules')
    parser = add_arguments(parser)
    return parser

def entrypoint(args=sys_argv[1:]):
    parser = build_parser()
    params = parser.parse_args(args)

    #create a temporary folder to make the connection between the
    #docker and the local files
    with tempfile.TemporaryDirectory() as tmpOutputFolder:
        command = ['/home/tool_RetroRules.py',
                   '-rule_type',
                   rule_type,
                   '-diameters',
                   diameters,
                   '-output_format',
                   output_format,
                   '-output',
                   '/home/tmp_output/output.dat']





##
#
#
if __name__ == "__main__":

    entrypoint(sys_argv[1:])
