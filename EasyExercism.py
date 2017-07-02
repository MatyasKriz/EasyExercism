#!/usr/bin/env python3

import re
import sys
import signal
import argparse
import subprocess
from os import walk


def signal_handler(signal, frame):
    if signal is signal.SIGINT:
        print('That\'s okay, see you later!')
        sys.exit(1)

signal.signal(signal.SIGINT, signal_handler)


def get_info(language):
    bash_command = "exercism fetch {}".format(language)
    output = subprocess.check_output(['bash', '-c', bash_command])

    project_name = ''
    path = ''
    is_new_problem = True
    for line in output.decode("utf-8").split('\n'):
        if line.startswith(language):
            try:
                project_name = re.search('\(([^\)]+)\)', line).group(1)
                path = re.search('\/\s*(.*)$', line).group(0)
            except AttributeError:
                print('Problem with parsing project name and path to project')
                sys.exit(2)
        elif 'new: 0' in line:
            is_new_problem = False

    if not project_name:
        print('Couldn\'t find any project')
        sys.exit(2)

    file_name = project_name.replace(' ', '')
    return file_name, path, is_new_problem


def fetch_problem(language):
    bash_command = "exercism fetch {}".format(language)
    subprocess.call(['bash', '-c', bash_command])

    _, path, _ = get_info(language)

    generate_project(language, path)


def submit_solution(language, submit_all, suffix):
    file_name, path, is_new_problem = get_info(language)

    if is_new_problem:
        print('Detected that \'submit\' was called before \'fetch\'. Cowardly shutting down.')
        generate_project(language, path)
        sys.exit(1)

    file_suffixes = {"swift": "swift"}
    if suffix:
        file_suffix = suffix
    elif language in file_suffixes:
        file_suffix = file_suffixes[language]
    else:
        file_suffix = input('What suffix is your language using? ')

    if submit_all:
        bash_command = "exercism submit "
        (_, _, filenames) = walk(path).next()

        for file in filenames:
            bash_command += "{0}/Sources/{1}.{2} ".format(path, file, file_suffix)
    else:
        bash_command = "exercism submit {0}/Sources/{1}.{2}".format(path, file_name, file_suffix)
        subprocess.call(['bash', '-c', bash_command])


def generate_project(language, path):
    generate_commands = {"swift": "swift package -C {} generate-xcodeproj".format(path)}

    if language in generate_commands:
        bash_command = generate_commands[language]
        subprocess.call(['bash', '-c', bash_command])


parser = argparse.ArgumentParser(epilog='use -l or --language to give language name to script directly')
subparsers = parser.add_subparsers(dest='command')
subparser_fetch = subparsers.add_parser('fetch', help='fetch a new problem or get info about the current one')
subparser_fetch.add_argument('language', type=str, help='language you wish to use')
subparser_submit = subparsers.add_parser('submit', help='submit a solution to current problem')
subparser_submit.add_argument('language', type=str, help='language you wish to use')
subparser_submit.add_argument('-a', '--allFiles', help='use default name and don\'t ask for a new one', action='store_true')
subparser_submit.add_argument('-s', '--suffix', help='give file suffix to script directly')
args = parser.parse_args()

language = ''
if not hasattr(args, 'language'):
    language = input('Which language do you wish to exercise today? ')
else:
    language = args.language

if 'fetch' in args.command:
    fetch_problem(language)
elif 'submit' in args.command:
    submit_solution(language, args.allFiles, args.suffix)
else:
    print('Sorry, I don\'t understand. Try again?\n')
    parser.print_help()
    sys.exit(2)