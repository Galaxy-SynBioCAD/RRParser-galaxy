#!/usr/bin/env python3
"""
Created on June 03 2020

@author: Joan Hérisson
@description: Galaxy script to query RetroRules service

"""
# from tarfile import open as tarfile_open
from tempfile import TemporaryDirectory as tempfile_tempdir
from shutil import copy as shutil_copy
from brs_rr import RetroRules, build_parser

if __name__ == "__main__":

    # Parse arguments with the tool parser
    parser = build_parser()
    parser.add_argument('-outfile', type=str)
    params = parser.parse_args()

    # Process in a temporary folder that will be automatically removed after exit
    with tempfile_tempdir() as tmpdirname:

        # Run the tool
        result = RetroRules(params.rules_type, tmpdirname, params.diameters)

        # Copy results to the place expected by Galaxy
        shutil_copy(result, params.outfile)


        # # Format ouput data as expected by Galaxy
        # with tarfile_open(params.output, mode='w:gz') as tf:
        #     for name in os_listdir(tmpdirname):
        #         tf.add(tmpdirname+"/"+name, arcname=name)
