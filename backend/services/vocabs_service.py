import boto3
from botocore.exceptions import BotoCoreError, ClientError

from abc import ABC, abstractmethod

from typing import List

class BaseVocabsService(ABC):

    @abstractmethod
    def get_vocab(self, vocab_name: str) -> None:
        pass

    @abstractmethod
    def put_vocab(self, vocab: list[str], vocab_name: str) -> None:
        pass

    @abstractmethod
    def vocab_exists(self, vocab_name: str) -> bool:
        pass


class S3VocabsService(BaseVocabsService):

    def __init__(
        self,
        access_key: str,
        secret_key: str,
        endpoint_url: str,
        bucket_name: str,
    ):

        self.bucket_name = bucket_name

        session = boto3.session.Session()
        self.s3_client = session.client(
            service_name='s3',
            aws_access_key_id=access_key,
            aws_secret_access_key=secret_key,
            endpoint_url=endpoint_url,
        )

    def get_vocab(self, vocab_name: str) -> None:
        try:
            response = self.s3_client.get_object(
                Bucket=self.bucket_name,
                Key=vocab_name,
            )

            return response['Body']
        except (ClientError, BotoCoreError) as err:
            raise RuntimeError(f"Failed to fetch vocab file from S3: {err}")

    def put_vocab(self, vocab: list[str], vocab_name: str) -> None:
        try:
            body_text = "\n".join(vocab)

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=vocab_name,
                Body=body_text.encode('utf-8'),
                ContentType='text/plain',
            )
        except (ClientError, BotoCoreError) as err:
            raise RuntimeError(f"Failed to upload vocab to S3: {err}")

    def vocab_exists(self, vocab_name: str) -> bool:
        try:
            self.s3_client.head_object(
                Bucket=self.bucket_name,
                Key=vocab_name,
            )
            return True

        except ClientError as err:
            error_code = err.response.get('Error', {}).get('Code')

            if error_code in ('404', 'NoSuchKey', 'NotFound'):
                return False

            raise RuntimeError(f"Failed to check if vocab exists: {err}")

        except BotoCoreError as err:
            raise RuntimeError(f"Failed to check if vocab exists: {err}")