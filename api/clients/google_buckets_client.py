import uuid
import asyncio
from time import time
from datetime import datetime, timedelta
from pathlib import Path
from google.oauth2 import service_account
from google.cloud import storage
from typing import Dict, Optional
from api.shared.logger import Logger
from api.enums.bucket_name import BucketName
from api.shared.env_variable_manager import EnvVariableManager


class GoogleBucketsClient:

    def __init__(self, bucket_name: BucketName):
        self.logger = Logger('GoogleBucketsClient')
        self.env = EnvVariableManager()
        storage_account_file_path: str = self.env.load('STORAGE_ACCOUNT_FILE_PATH', 'auth/tudo-fresco-backend.json').string()
        self.signed_url_expiration_seconds: str = self.env.load('SIGNED_BUCKET_URL_EXPIRATION_SECONDS', 10800).integer()
        credentials = service_account.Credentials.from_service_account_file(storage_account_file_path)
        self.client = storage.Client(credentials=credentials)
        self.logger.log_info(f'Using the bucket {bucket_name.value}')
        self.bucket = self.client.bucket(bucket_name.value)
        self.image_directory = 'images'
        self.manager = GoogleStorageClientCacheManager()

    def _generate_unique_filename(self, original_filename: str, folder: Optional[str] = '') -> str:
        ext = Path(original_filename).suffix
        timestamp = int(time())
        unique_name = f'{timestamp}_{uuid.uuid4()}{ext}'
        name = f'{folder}/{unique_name}'
        self.logger.log_debug(f'File name generated: {name}')
        return name

    async def save_image(self, image_bytes: bytes, original_filename: str) -> str:
        self.logger.log_debug(f'Saving image, original name: {original_filename}')
        blob_name = self._generate_unique_filename(original_filename, self.image_directory)
        blob = self.bucket.blob(blob_name)
        await asyncio.to_thread(blob.upload_from_string, image_bytes, content_type=self._get_content_type(original_filename))
        self.logger.log_debug(f'Image saved with blob name: {blob_name}')
        return blob_name

    async def delete_image(self, blob_name: str) -> None:
        self.logger.log_debug(f'Deleting image, file name: {blob_name}')
        blob = self.bucket.blob(blob_name)
        self.manager.remove_cache(blob.name)
        await asyncio.to_thread(blob.delete)

    async def update_image(self, new_image_bytes: bytes, original_filename: str, old_blob_name: Optional[str] = None) -> str:
        self.logger.log_debug(f'Updating image, old file name: {old_blob_name}')
        if old_blob_name and old_blob_name.strip():
            await self.delete_image(old_blob_name)
            self.manager.remove_cache(old_blob_name)
        return await self.save_image(new_image_bytes, original_filename)

    async def read_image(self, blob_name: str) -> str:
        if not blob_name:
            return ''
        cached_signed_url = self.manager.get_image_signed_url(blob_name)
        if cached_signed_url:
            return cached_signed_url
        blob = self.bucket.blob(blob_name)
        expiration: timedelta = timedelta(seconds=self.signed_url_expiration_seconds)
        signed_url: str = await asyncio.to_thread(blob.generate_signed_url, 
                                      version='v4', 
                                      expiration=expiration,
                                      method='GET')
        self.manager.cache_image(blob_name, signed_url, expiration)
        return signed_url

    def _get_content_type(self, filename: str) -> str:
        ext = Path(filename).suffix.lower()
        return {
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.png': 'image/png',
            '.webp': 'image/webp'
        }.get(ext, 'application/octet-stream')
    
class GoogleStorageClientCacheImage:

    def __init__(self, blob_name: str, signed_url: str, expiration: timedelta):
        self.blob_name: str = blob_name
        self.signed_url: str = signed_url
        self.expires_at: datetime = datetime.now() + expiration

    def is_expired(self) -> bool:
        return datetime.now() >= self.expires_at

class GoogleStorageClientCacheManager:

    def __init__(self):
        self.cached: Dict[str, GoogleStorageClientCacheImage] = {}

    def cache_image(self, blob_name: str, signed_url: str, expiration: timedelta) -> None:
        self.cached[blob_name] = GoogleStorageClientCacheImage(blob_name, signed_url, expiration)

    def remove_cache(self, blob_name: str) -> None:
        del self.cached[blob_name]

    def get_image_signed_url(self, blob_name: str) -> Optional[str]:
        cached_image = self.cached.get(blob_name)
        if not cached_image:
            return None
        if cached_image.is_expired():
            self.remove_cache(blob_name)
            return None
        return cached_image.signed_url