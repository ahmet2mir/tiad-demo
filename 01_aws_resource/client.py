from __future__ import absolute_import

import time
import client_provider
import celry


if __name__ == '__main__':
    
    action = "create"
    hostname = "hostname-00012"
    resource = {
        "return": [
            "uuid",
            "name",
            "public_dns"
        ],
        "name": "instance",
        "outputs": "None",
        "require": "None",
        "properties": {
            "image_id": "ami-1f198668",
            "name": hostname,
            "instance_type": "t2.medium",
            "subnet_id": "subnet-364e0470",
            "key_name": "key-demo-tiad-ahmet",
            "security_group_ids": "sg-edc4bf88"
        },
        "returns": "None",
        "version": "v001",
        "provider": {
            "version": "v001",
            "name": "aws",
            "properties": {
                "name": "aws",
                "@timestamp": "2015-03-18T16:35:07.468Z",
                "version": "v001",
                "aws_secret_access_key": client_provider.aws_secret_access_key,
                "region": "eu-west-1",
                "_id": "aws-v001",
                "aws_access_key_id": client_provider.aws_access_key_id
            }
        },
        "lifecycle": action,
        "type": "instance",
        "id": "eef2329954d"
    }

    # send task to broker
    rex_task = celry.app.send_task("rex.tasks.run", [resource])

    # wait end task
    timeout = 500
    i = 0
    while not rex_task.ready() and i < timeout:
        i = i + 2
        time.sleep(2)

    if i >= timeout:
        print("Resource %s timeout" % resource["name"])

    # status
    if rex_task.successful()\
            and rex_task.result\
            and "status" in rex_task.result\
            and rex_task.result["status"]:
        resource["outputs"] = rex_task.result["response"]
        print(rex_task.result["response"])
    else:
        print(rex_task.traceback)
