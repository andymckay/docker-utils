import logging
import os

import yaml

# For reference see: https://docs.docker.com/compose/yml/
allowed_service_commands = [
    'build', 'cap_add', 'cap_drop', 'command',
    'cpu_shares', 'dns', 'dns_search', 'domainname', 'entrypoint', 'env_file',
    'environemnt', 'expose', 'extends', 'external_links', 'hostname', 'image',
    'links', 'mem_limit', 'net', 'pid', 'post', 'ports', 'privileged', 'restart',
    'stdin_open', 'tty', 'user', 'volumes', 'volumes_from', 'working_dir'
]

log = logging.getLogger(__name__)

error_descriptions = {'E01': 'Unknown option'}


def lint(command, project, options):
    path = command.get_config_path(
        options.get('--file')
        or os.environ.get('COMPOSE_FILE')
        or os.environ.get('FIG_FILE'))

    errors = []
    data = yaml.safe_load(open(path, 'r'))
    for node, entries in data.items():
        for key in entries.keys():
            if key not in allowed_service_commands:
                errors.append(('E01', key))

    for error, key in errors:
        log.info('{f}: {e} {d} "{k}"'.format(
            f=path, e=error, d=error_descriptions[error], k=key
        ))
