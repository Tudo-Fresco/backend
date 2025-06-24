import unittest
from unittest.mock import patch, AsyncMock, MagicMock
from api.clients.google_buckets_client import GoogleBucketsClient
from api.enums.bucket_name import BucketName
from api.shared.logger import Logger
from api.shared.env_variable_manager import EnvVariableManager


class TestGoogleBucketsClient(unittest.IsolatedAsyncioTestCase):

    def setUp(self) -> None:
        self.bucket_name = BucketName.PRODUCT_IMAGES

    @patch.object(Logger, 'log_info')
    @patch.object(EnvVariableManager, 'load')
    @patch('google.oauth2.service_account.Credentials.from_service_account_file')
    @patch('google.cloud.storage.Client')
    def test_init_sets_up_correctly(self, mock_storage_client_cls, mock_credentials: MagicMock, mock_env_load: MagicMock, mock_log_info: MagicMock) -> None:
        mock_env_load.side_effect = [MagicMock(string=lambda: 'fake/path.json'), MagicMock(integer=lambda: 10800)]
        mock_client = MagicMock()
        mock_bucket = MagicMock()
        mock_client.bucket.return_value = mock_bucket
        mock_storage_client_cls.return_value = mock_client
        client = GoogleBucketsClient(self.bucket_name)
        mock_log_info.assert_called_with(f'Using the bucket {self.bucket_name.value}')
        self.assertEqual(client.bucket, mock_bucket)

    @patch('api.clients.google_buckets_client.time', return_value=1234567890)
    @patch('api.clients.google_buckets_client.uuid.uuid4', return_value='uuid')
    def test_generate_unique_filename(self, mock_uuid: MagicMock, mock_time: MagicMock) -> None:
        client = GoogleBucketsClient(BucketName.PRODUCT_IMAGES)
        result = client._generate_unique_filename('image.png', 'folder')
        self.assertTrue(result.startswith('folder/1234567890_uuid'))
        self.assertTrue(result.endswith('.png'))

    @patch.object(GoogleBucketsClient, '_get_content_type', return_value='image/png')
    @patch('google.cloud.storage.Blob.upload_from_string')
    @patch('google.cloud.storage.Client.bucket')
    async def test_save_image_uploads_image(self, mock_bucket, mock_upload: MagicMock, mock_get_content_type: MagicMock) -> None:
        mock_blob = MagicMock()
        mock_bucket.return_value.blob.return_value = mock_blob
        client = GoogleBucketsClient(self.bucket_name)
        client.bucket = mock_bucket.return_value
        result = await client.save_image(b'data', 'image.png')
        self.assertTrue(result.endswith('.png'))
        mock_blob.upload_from_string.assert_called_once()

    @patch('google.cloud.storage.Client.bucket')
    async def test_delete_image_blob_not_found(self, mock_bucket: MagicMock) -> None:
        client = GoogleBucketsClient(self.bucket_name)
        client.bucket = mock_bucket.return_value
        client.manager = MagicMock()
        mock_bucket.return_value.get_blob.return_value = None
        await client.delete_image('nonexistent.png')
        client.manager.remove_cache.assert_not_called()

    @patch('google.cloud.storage.Client.bucket')
    async def test_delete_image_success(self, mock_bucket: MagicMock) -> None:
        mock_blob = MagicMock()
        mock_blob.name = 'exists.png'
        mock_bucket.return_value.get_blob.return_value = mock_blob
        client = GoogleBucketsClient(BucketName.PRODUCT_IMAGES)
        client.bucket = mock_bucket.return_value
        client.manager = MagicMock()
        await client.delete_image('exists.png')
        client.manager.remove_cache.assert_called_once_with('exists.png')
        mock_blob.delete.assert_called_once()

    @patch.object(GoogleBucketsClient, 'save_image', new_callable=AsyncMock, return_value='new_blob.png')
    @patch.object(GoogleBucketsClient, 'delete_image', new_callable=AsyncMock)
    async def test_update_image_with_old_blob(self, mock_delete_image: MagicMock, mock_save_image: MagicMock) -> None:
        client = GoogleBucketsClient(self.bucket_name)
        client.manager = MagicMock()
        result = await client.update_image(b'data', 'img.png', 'old_blob.png')
        mock_delete_image.assert_awaited_once_with('old_blob.png')
        client.manager.remove_cache.assert_called_once_with('old_blob.png')
        self.assertEqual(result, 'new_blob.png')

    @patch('google.cloud.storage.Blob.generate_signed_url')
    @patch('google.cloud.storage.Client.bucket')
    async def test_read_image_cache_miss(self, mock_bucket: MagicMock, mock_signed_url: MagicMock) -> None:
        client = GoogleBucketsClient(self.bucket_name)
        client.manager = MagicMock(get_image_signed_url=lambda _: None)
        mock_blob = MagicMock()
        mock_signed_url.return_value = 'http://signed-url'
        mock_blob.generate_signed_url.return_value = 'http://signed-url'
        mock_bucket.return_value.blob.return_value = mock_blob
        client.bucket = mock_bucket.return_value
        result = await client.read_image('img.png')
        self.assertEqual(result, 'http://signed-url')
        client.manager.cache_image.assert_called_once()

    async def test_read_image_cache_hit(self) -> None:
        client = GoogleBucketsClient(self.bucket_name)
        client.manager = MagicMock(get_image_signed_url=lambda _: 'cached-url')
        result = await client.read_image('img.png')
        self.assertEqual(result, 'cached-url')

    def test_get_content_type(self) -> None:
        client = GoogleBucketsClient(self.bucket_name)
        self.assertEqual(client._get_content_type('photo.JPG'), 'image/jpeg')
        self.assertEqual(client._get_content_type('file.webp'), 'image/webp')
        self.assertEqual(client._get_content_type('unknown.txt'), 'application/octet-stream')
