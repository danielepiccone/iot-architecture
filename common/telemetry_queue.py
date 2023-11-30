import boto3
import logging
import time
import json

queue = None

SQS_QUEUE_NAME = "telemetry.fifo"


def _create_queue():
    global queue

    try:
        sqs = boto3.resource("sqs")
        queue = sqs.create_queue(
            QueueName=SQS_QUEUE_NAME,
            Attributes={"FifoQueue": "true", "ContentBasedDeduplication": "true"},
        )
    except:
        queue = sqs.get_queue_by_name(QueueName=SQS_QUEUE_NAME)


class SQSWorker:
    logger = logging.getLogger(__name__)

    def __init__(self):
        self.sqs = boto3.client("sqs")
        self.queue_url = queue.url
        self.polling_delay = 0.1
        self.max_number_of_messages = 10

    def run(self, processor_fn):
        self.logger.info(f"Starting SQS worker from {self.queue_url}")
        while True:
            response = self.sqs.receive_message(
                QueueUrl=self.queue_url, MaxNumberOfMessages=self.max_number_of_messages
            )

            if "Messages" in response:
                for message in response["Messages"]:
                    self.logger.info("Processing message: " + message["MessageId"])
                    try:
                        processor_fn(json.loads(message["Body"]))
                        self.sqs.delete_message(
                            QueueUrl=self.queue_url,
                            ReceiptHandle=message["ReceiptHandle"],
                        )
                        self.logger.info(
                            "Successfully processed message " + message["MessageId"]
                        )
                    except Exception as e:
                        self.logger.exception(e)

                    time.sleep(self.polling_delay)

    def enqueue(self, message, group_id):
        self.sqs.send_message(
            QueueUrl=self.queue_url,
            MessageBody=json.dumps(message),
            MessageGroupId=group_id,
        )


_create_queue()
