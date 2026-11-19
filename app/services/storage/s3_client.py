from contextlib import asynccontextmanager
from aiobotocore.session import get_session
from ...core.config import s3_settings
class S3Client:
    def __init__(self,
                 access_key: str,
                 secret_key: str,
                 endpoint_url: str,
                 bucket_name: str,
                 public_url: str
                 ):
    
        self.config = {
            "aws_access_key_id": access_key,
            "aws_secret_access_key": secret_key,
            "endpoint_url": endpoint_url,
            "region_name": "auto"
        }
        self.bucket_name = bucket_name
        self.public_url = public_url
        self.session = get_session()

    @asynccontextmanager
    async def get_client(self):
        async with self.session.create_client("s3", **self.config) as client:
            yield client

    async def upload_file(
            self, 
            file_data: bytes, 
            object_name: str,
            content_type: str = "image/jpeg"
    ):
        
        async with self.get_client() as client:
            await client.put_object(
                Bucket=self.bucket_name,
                Key=object_name,
                Body=file_data,
                ContentType=content_type
            )

    async def delete_file(self, object_name: str):
        async with self.get_client() as client:
            await client.delete_object(
                Bucket=self.bucket_name,
                Key=object_name
            )

    async def get_public_url(self):
        return self.public_url
    
async def get_s3():
    s3 = S3Client(
        access_key=s3_settings.s3_access_key.get_secret_value(),
        secret_key=s3_settings.s3_secret_key.get_secret_value(),
        endpoint_url=s3_settings.s3_endpoint_url,
        bucket_name=s3_settings.s3_bucket_name,
        public_url=s3_settings.s3_public_url
    )
    return s3