

def get_queue_url(sqs_client, queue_name: str) -> str:
    resp = sqs_client.get_queue_url(QueueName=queue_name)
    return resp["QueueUrl"]