import logging

from campuslibs.aws.s3 import S3Utility

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def download(s3_utility: S3Utility, object, local_path):
    logger.info(f'downloading... {object}')
    s3_utility.download(object, local_path)


def upload(s3_utility: S3Utility, local_path, s3_folder):
    obj_path = s3_utility.upload(local_path, upload_folder=s3_folder, unique_filename=False, stream=False, public=False)
    # logger.info(f"uploaded: {obj_path}")
    return obj_path


def upload_object(s3_utility: S3Utility, data, s3_folder, filename):
    # ToDo: implement. Example: data={'a':20}
    pass


def the_bucket_list(s3):
    """ https://www.imdb.com/title/tt0825232/ """

    for key in s3.get_objects_list():
        yield key['Key']
