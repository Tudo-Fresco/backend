from enum import Enum


class BucketName(str, Enum):
    USER_PROFILE = 'user-profiles-images'
    PRODUCT_IMAGES = 'product-portfolio-images'
    STORE_PICTURES = 'store-catalog-images'