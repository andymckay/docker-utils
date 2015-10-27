import os

from compose.project import NoSuchService


class NoContainer(NoSuchService):
    def __init__(self, name):
        self.name = name
        self.msg = "No container for: %s" % self.name

    def __str__(self):
        return self.msg


def get_service(project):
    cur = os.getcwd()

    def walk(directory):
        if 'Dockerfile' in os.listdir(directory):
            return os.path.basename(directory)

        new = os.path.dirname(directory)
        if new == directory:
            raise NoSuchService(cur)
        return walk(new)

    service = walk(cur)
    if service not in [s.name for s in project.services]:
        raise NoSuchService(service)

    return service


def get_container(project, service):
    print project.containers()
    containers = project.containers(service_names=[service])
    if not containers:
        raise NoContainer(service)
    return containers[0]


def get_images(project):
    return [s for s in project.services if not s.can_be_built()]
