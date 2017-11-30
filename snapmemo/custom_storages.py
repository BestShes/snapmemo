from storages.backends.s3boto import S3BotoStorage

from snapmemo import settings


class MediaStorage(S3BotoStorage):
    location = settings.MEDIAFILES_LOCATION
