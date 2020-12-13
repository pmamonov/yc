import yandexcloud
from yandex.cloud.compute.v1.instance_service_pb2_grpc import InstanceServiceStub
from yandex.cloud.compute.v1.instance_service_pb2 import (
	ListInstancesRequest,
	StartInstanceRequest
)

def sdk(sa_key):
	return yandexcloud.SDK(service_account_key=sa_key)

def find_name(records, name):
    for record in records:
        if record.name == name:
            return record

def list_instances(sdk, folder):
    service = sdk.client(InstanceServiceStub)
    return service.List(
        ListInstancesRequest(
            folder_id=folder
        )
    ).instances

def find_instance(sdk, folder, name):
    instances = list_instances(sdk, folder)
    return find_name(instances, name)

def instance_ip(instance):
    for interface in instance.network_interfaces:
        return interface.primary_v4_address.one_to_one_nat.address

def instance_start(sdk, ins):
    service = sdk.client(InstanceServiceStub)
    service.Start(StartInstanceRequest(instance_id = ins.id))

if __name__ == "__main__":
	import conf
	from time import sleep
	from sys import stderr

	_sdk = sdk(conf.sa_key)
	while 1:
		ins = find_instance(_sdk, conf.FOLDER_ID, conf.INST_NAME)
		if ins.status == ins.RUNNING:
			stderr.write("RUNNING %s\n" % instance_ip(ins))
			break
		elif ins.status == ins.STOPPED:
			stderr.write("STOPPED\n")
		else:
			stderr.write("status %d\n" % ins.status)

		sleep(10)

	print(instance_ip(ins))
