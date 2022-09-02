import dataclasses
import os
from time import sleep
from typing import Iterable
from typing import List

import yandexcloud
from yandex.cloud.compute.v1.instance_pb2 import Instance
from yandex.cloud.compute.v1.instance_service_pb2 import (
    ListInstancesRequest,
)
from yandex.cloud.compute.v1.instance_service_pb2 import StartInstanceRequest
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.resourcemanager.v1.folder_service_pb2 import ListFoldersRequest
from yandex.cloud.resourcemanager.v1.folder_service_pb2_grpc import FolderServiceStub

YANDEX_CLOUD_TOKEN = os.environ.get('YANDEX_CLOUD_TOKEN')
YANDEX_CLOUD_ID = os.environ.get('YANDEX_CLOUD_ID')
PROXY_FILES_PATH = os.environ.get('PROXY_FILES_PATH', '/scripts/files/')


@dataclasses.dataclass
class YandexSDK(object):

    token: str
    cloud_id: str

    def __post_init__(self):
        sdk = yandexcloud.SDK(token=YANDEX_CLOUD_TOKEN)

        self._instance_service = sdk.client(InstanceServiceStub)
        self._folder_service = sdk.client(FolderServiceStub)

    def instances(self) -> Iterable[Instance]:
        for folder in self._folder_service.List(ListFoldersRequest(cloud_id=self.cloud_id)).folders:

            for instance in self._instance_service.List(ListInstancesRequest(folder_id=folder.id)).instances:
                yield instance

    def list_instances_ips(self) -> List[str]:
        cloud_instances_ips = []
        for instance in self.instances():
            cloud_instances_ips.append(
                instance.network_interfaces[0].primary_v4_address.one_to_one_nat.address,
            )

        return cloud_instances_ips

    def run_stopped_instances(self):
        for instance in self.instances():
            if instance.status == instance.STOPPED:
                print(f'Stopped instance detected {instance.id}, starting...')
                self._instance_service.Start(StartInstanceRequest(instance_id=instance.id))

    def run_stopped_and_list_ips(self):
        self.run_stopped_instances()
        while True:
            instances_status = set([instance.status for instance in self.instances()])
            if len(instances_status) == 1 and list(instances_status)[0] == 2:
                return self.list_instances_ips()
            print('Waiting for provisioning...')
            sleep(3)


if __name__ == '__main__':
    cloud_service = YandexSDK(
        token=YANDEX_CLOUD_TOKEN,
        cloud_id=YANDEX_CLOUD_ID,
    )
    proxies = cloud_service.run_stopped_and_list_ips()
    print(f'{len(proxies)} new ips got: {proxies}')
    with open(f'{PROXY_FILES_PATH}/constant-proxies.txt', 'w') as f:
        for proxy in proxies:
            f.write(f'{proxy}:3128\n')
