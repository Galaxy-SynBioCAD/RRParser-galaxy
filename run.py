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
# from tarfile import open as tarfile_open
# from tarfile import TarInfo as tarfile_TarInfo
from tempfile import TemporaryDirectory as tempfile_tempdir
from os import listdir as os_listdir
from shutil import move as shutil_move
from zipfile import ZipFile as zf



if __name__ == "__main__":

    # Parse arguments with the tool parser
    parser = tool_buildparser()
    params = parser.parse_args()

    # Process in a temporary folder that will be automatically removed after exit
    with tempfile_tempdir() as tmpdirname:

        # Prepare arguments for the tool
        args = [
            '-rules_type', params.rules_type,
            '-output', tmpdirname,
            '-diameters', params.diameters
            ]

        # Run the tool
        outfile = tool_entrypoint(args)

        # shutil_move(outfile, params.output)

        zip = zf(params.output, 'w')
        zip.write(outfile, compress_type=zipfile.ZIP_DEFLATED)
        zip.close()

        # # Format ouput data as expected by Galaxy
        # with tarfile_open(params.output, mode='w:gz') as tf:
        #     for name in os_listdir(tmpdirname):
        #         tf.add(tmpdirname+"/"+name, arcname=name)
