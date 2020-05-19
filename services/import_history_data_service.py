import json
import logging
import os
from abc import ABCMeta, abstractmethod

from campuslibs.aws.s3 import S3Utility
from models.history.import_history import ImportHistoryData
from mongoengine import NotUniqueError

from utils import file_utils, s3_utils
from utils.constants import Constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImporterHistoryDataServiceBaseClass(metaclass=ABCMeta):
    def __init__(self, import_history, importer, config):
        self.importer = importer

        self.import_history = import_history
        self._config = config

        self.load_importer_specific_services()

        if self._config.S3_ENABLED:
            self.s3 = S3Utility(self._config.AWS_ACCESS_KEY_ID,
                                self._config.AWS_SECRET_ACCESS_KEY,
                                self._config.AWS_RAW_IMPORT_DATA_BUCKET)

    @staticmethod
    def save(data):
        try:
            data.save()
        except NotUniqueError as e:
            logger.error(f"NotUniqueError: on '{data.key_name}' for code={data.data_object_id}")
            pass
        except Exception as e:
            logger.error(f"Error on saving {data.key_name} data: id={data.data_object_id} \n{str(e)}")

    def dump(self, data):
        if not self._config.DUMP_ENABLED:
            return

        try:
            filename = data.data_object_id + ".json"
            local_dir = os.path.join(Constants.FILES, Constants.API, data.key_name)
            if not os.path.exists(local_dir):
                os.mkdir(local_dir)
            local_path = os.path.join(local_dir, filename)

            # save locally
            with open(local_path, 'w') as file_:
                file_.write(json.dumps(data.data_object))

            # upload to s3
            if self._config.S3_ENABLED:
                date_folder = file_utils.folder_structure_from_date(self.import_history.importer_start_time)
                s3_folder = os.path.join(self.importer.name, self.importer.code, date_folder, data.key_name)
                s3_utils.upload(self.s3, local_path, s3_folder)

        except Exception as e:  # ToDo: Separate error logs for each dumping to db/file/s3
            logger.error("Error on dumping {} data: id={} \n{}".format(
                data.key_name, data.data_object_id, str(e)))

    def create_import_history_data(self, data_dict, key_name, data_object_id):
        return ImportHistoryData(
            history=self.import_history.id,  # Assign object for ReferenceField?
            key_name=key_name,
            data_object_id=data_object_id,
            data_object=data_dict
        )

    @abstractmethod
    def load_importer_specific_services(self):
        raise NotImplementedError
