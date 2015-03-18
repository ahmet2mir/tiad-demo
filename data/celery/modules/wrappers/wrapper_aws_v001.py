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

from aws_v001.instance import Instance


def create_instance(provider, resource):

    i = Instance(provider["region"],
                 provider["aws_access_key_id"],
                 provider["aws_secret_access_key"])
    out = i.create(resource["name"],\
                   resource["image_id"],\
                   resource["key_name"],\
                   resource["instance_type"],\
                   resource["security_group_ids"],\
                   resource["subnet_id"])
    return out


def delete_instance(provider, resource):
    i = Instance(provider["region"],
                 provider["aws_access_key_id"],
                 provider["aws_secret_access_key"])
    out = i.delete(resource["name"])
    return out


def read_instance(provider, resource):
    i = Instance(provider["region"],
                 provider["aws_access_key_id"],
                 provider["aws_secret_access_key"])
    out = i.read(resource["name"])
    return out


if __name__ == '__main__':

    provider = {"region": "eu-west-1",
                "aws_access_key_id": 'xxxx',
                "aws_secret_access_key": 'xxxx'}

    resource = {"image_id": "ami-xxxx",
                "key_name": "xxxx",
                "instance_type": "t2.medium",
                "security_group_ids": "sg-xxxx",
                "subnet_id": "subnet-xxxx"}

    resource["name"] = "hostname-0005"


    print read_instance(provider, resource)
    print create_instance(provider, resource)

    import time
    time.sleep(5)

    print delete_instance(provider, resource)
    print read_instance(provider, resource)

