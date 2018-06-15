from __future__ import print_function, unicode_literals

import io
import subprocess
from argparse import ArgumentParser

try:
    prompt = raw_input
except NameError:
    prompt = input


parser = ArgumentParser()
parser.add_argument(
    '-r', '--requirements', type=str, default='requirements.txt',
    help='Specify the location of the requirements.txt file')


def get_installed_requirement(entry):
    installed_name, installed_version = None, None

    name = entry.split('[', 1)[0]
    info = (subprocess.check_output(['pip', 'show', name.strip()])
            .decode('utf-8', 'replace'))
    for line in info.split('\n'):
        line = line.strip()
        if 'Name: ' in line:
            installed_name = line[len('Name: '):]
        if 'Version: ' in line:
            installed_version = line[len('Version: '):]

    if not installed_name or not installed_version:
        raise ValueError('Could not info for {!r}'.format(entry))

    return entry.replace(name, installed_name, 1), installed_version


def main(args=None):
    args = parser.parse_args(args)

    # Read pinned requirements
    try:
        with io.open(args.requirements) as f:
            print('Reading {}...'.format(args.requirements))
            requirements = [r.split('#', 1)[0].strip() for r in f.readlines()]
    except:
        print('Error: No requirements.txt found')
        return

    # Get names of requirements to run 'pip install --upgrade' on
    upgrades = []
    for requirement in requirements:
        if not requirement:
            continue
        # TODO: Handle other version instructions
        if '==' not in requirement:
            print('Error: Can only work with pinned requirements for now.')
        name, version = requirement.split('==')
        upgrades.append(name)

    # Edge case
    if len(upgrades) == 0:
        print('No requirements to upgrade')
        return

    # Confirm
    answer = prompt('Upgrade {} requirements (y/N)? '.format(len(upgrades)))
    if answer != 'y':
        return
    print()

    # Run 'pip install --upgrade' on all requirements
    for name in upgrades:
        print('$ pip install --upgrade', name)
        exit_code = subprocess.call(['pip', 'install', '--upgrade', name])
        if exit_code != 0:
            return
        print()

    # Show message
    print('Collecting installed versions...')

    # Generate resulting requirements.txt content
    result = ''
    for name in upgrades:
        installed_name, installed_version = get_installed_requirement(name)
        result = '{}{}=={}\n'.format(result, installed_name, installed_version)

    # Save upgraded requirements
    with io.open(args.requirements, 'w') as f:
        f.write(result)

    print('Wrote {}'.format(args.requirements))


if __name__ == '__main__':
    main()
