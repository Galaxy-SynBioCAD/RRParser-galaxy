#!/usr/bin/env python3
"""
Created on June 03 2020

@author: Joan Hérisson
@description: Galaxy script to query RetroRules service

"""
# from tarfile import open as tarfile_open
from tempfile import TemporaryDirectory as tempfile_tempdir
from shutil import copy as shutil_copy
from rr_parser import RRulesParser, build_args_parser

if __name__ == "__main__":

    # Parse arguments with the tool parser
    parser = build_args_parser()
    parser.add_argument('--output_format_galaxy',
                            type=str,
                            choices=['csv', 'tar'])
    params = parser.parse_args()

    # Process in a temporary folder that will be automatically removed after exit
    with tempfile_tempdir() as tmpdirname:

        if params.output_format_galaxy=='tar': params.output_format = 'tar.gz'
        # Run the tool
        result_file = RRulesParser().parse_rules(params.rule_type, tmpdirname, params.diameters, params.output_format)

        # Copy results to the place expected by Galaxy
        shutil_copy(result_file, params.output_folder)
