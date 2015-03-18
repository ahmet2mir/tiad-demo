import logging

# Set Logger
LOGGER = logging.getLogger("aws_v001")
console_formatter = logging.Formatter(
            '%(filename)s:%(lineno)d\t\t\t%(message)s', '%m-%d %H:%M:%S')
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
console_handler.setFormatter(console_formatter)
LOGGER.addHandler(console_handler)
LOGGER.setLevel(10)

# Set the path
import os, sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from docker_v001.container import Container


def create_container(provider, resource):

    i = Container(resource["host"],
                 resource["port"])
    out = i.create(resource["name"],\
                   resource["image"],\
                   resource["ports"])
    return out

def delete_container(provider, resource):
    i = Container(resource["host"],
                 resource["port"])
    out = i.delete(resource["name"])
    return out


def read_container(provider, resource):
    i = Container(resource["host"],
                 resource["port"])
    out = i.read(resource["name"])
    return out


if __name__ == '__main__':

    provider = {"host": "ec2-xxxxx.eu-west-1.compute.amazonaws.com",
    			"port":"2375"}

    resource = {"image": "ahmet2mir/jenkins",
                "ports": {80: 80, 8080: 8080}}

    resource["name"] = "jenkins"

    print read_container(provider, resource)
    print create_container(provider, resource)

    import time
    time.sleep(5)

    print delete_container(provider, resource)
    print read_container(provider, resource)

