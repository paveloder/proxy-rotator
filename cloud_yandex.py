import os
from typing import List

import yandexcloud

from yandex.cloud.resourcemanager.v1.folder_service_pb2 import ListFoldersRequest
from yandex.cloud.resourcemanager.v1.folder_service_pb2_grpc import FolderServiceStub
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.instance_service_pb2 import (
    ListInstancesRequest,
)

YANDEX_CLOUD_TOKEN = os.environ.get('YANDEX_CLOUD_TOKEN')
YANDEX_CLOUD_ID = os.environ.get('YANDEX_CLOUD_ID')


def get_cloud_instances_ips() -> List[str]:
    sdk = yandexcloud.SDK(token=YANDEX_CLOUD_TOKEN)

    instance_service = sdk.client(InstanceServiceStub)
    folder_service = sdk.client(FolderServiceStub)
    cloud_instances_ips = []
    for folder in folder_service.List(ListFoldersRequest(cloud_id=YANDEX_CLOUD_ID)).folders:

        for instance in instance_service.List(ListInstancesRequest(folder_id=folder.id)).instances:
            cloud_instances_ips.append(instance.network_interfaces[0].primary_v4_address.one_to_one_nat.address)

    return cloud_instances_ips


with open('/scripts/files/constant-proxies.txt', 'w') as f:
    for proxy in get_cloud_instances_ips():
        f.write(f'{proxy}:3128\n')
