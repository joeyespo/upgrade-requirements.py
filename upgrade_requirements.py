from __future__ import print_function, unicode_literals

import io
import subprocess

try:
    prompt = raw_input
except NameError:
    prompt = input


def get_installed_requirement(entry):
    installed_name, installed_version = None, None

    name = entry.split('[', 1)[0]
    info = (subprocess.check_output(['pip', 'show', name])
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


def main():
    # Read pinned requirements
    try:
        with io.open('requirements.txt') as f:
            print('Reading requirements...')
            requirements = [r.strip() for r in f.readlines()]
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
    with io.open('requirements.txt', 'w') as f:
        f.write(result)

    print('Wrote requirements.txt')


if __name__ == '__main__':
    main()
