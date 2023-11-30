import boto3
import json

BUCKET_NAME = "telemetry-data"


def _create_bucket():
    s3 = boto3.resource("s3")
    s3.create_bucket(Bucket=BUCKET_NAME)


class TelemetryService:
    def __init__(self):
        self.s3 = boto3.client("s3")
        self.bucket_name = BUCKET_NAME

    def put(self, file_name, json_string):
        self.s3.put_object(Body=json_string, Bucket=self.bucket_name, Key=file_name)

    def list(self, path):
        response = self.s3.list_objects_v2(Bucket=self.bucket_name, Prefix=path)
        json_files = []
        for obj in response.get("Contents", []):
            if obj["Key"].endswith(".json"):
                file_content = (
                    self.s3.get_object(Bucket=self.bucket_name, Key=obj["Key"])["Body"]
                    .read()
                    .decode("utf-8")
                )
                json_data = json.loads(file_content)
                json_files.append(json_data)
        return json_files


_create_bucket()
