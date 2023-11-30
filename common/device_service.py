import boto3
import json

DEVICES_TABLE_NAME = "devices"


def _create_table():
    dynamodb = boto3.resource("dynamodb")

    try:
        dynamodb.create_table(
            TableName=DEVICES_TABLE_NAME,
            KeySchema=[{"AttributeName": "id", "KeyType": "HASH"}],
            AttributeDefinitions=[{"AttributeName": "id", "AttributeType": "S"}],
            ProvisionedThroughput={"ReadCapacityUnits": 5, "WriteCapacityUnits": 5},
        )
        dynamodb.meta.client.get_waiter("table_exists").wait(
            TableName=DEVICES_TABLE_NAME
        )
    except:
        pass


class DeviceService:
    def __init__(self):
        self.table_name = DEVICES_TABLE_NAME
        self.dynamodb = boto3.resource("dynamodb")
        self.table = self.dynamodb.Table(self.table_name)

    def create_device(self, device_id, state):
        item = {"id": device_id, "state": state}
        self.table.put_item(Item=item)

    def get_device(self, device_id):
        response = self.table.get_item(Key={"id": device_id})
        item = response.get("Item")
        if item:
            return json.loads(item["state"])
        return None

    def update_device(self, device_id, state):
        item = {"id": device_id, "state": state}
        self.table.put_item(Item=item)

    def delete_device(self, device_id):
        self.table.delete_item(Key={"id": device_id})

    def list_devices(self):
        response = self.table.scan()
        return [json.loads(item["state"]) for item in response["Items"]]


_create_table()
