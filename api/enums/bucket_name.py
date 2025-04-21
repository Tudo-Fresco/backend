from enum import Enum


class BucketName(str, Enum):
    USER_PROFILE = 'user-profiles-images'
    PRODUCT_IMAGES = 'product-images'
    STORE_PICTURES = 'store-images'