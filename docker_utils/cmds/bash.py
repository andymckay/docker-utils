import os

from . import utils


def bash(project, options):
    service = options['SERVICE'] or utils.get_service(project)
    print project, service, options
    container = utils.get_container(project, service)
    cmd = 'docker exec -t -i {0} /bin/bash'.format(container.id)
    os.system(cmd)
