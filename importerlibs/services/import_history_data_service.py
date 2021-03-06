import json
import logging
import os
from abc import ABCMeta, abstractmethod

from campuslibs.aws.s3 import S3Utility
from models.history.import_history import ImportHistoryData
from mongoengine import NotUniqueError

from importerlibs.utils import file_utils, s3_utils
from importerlibs.utils.constants import Constants

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImporterHistoryDataServiceBaseClass(metaclass=ABCMeta):
    """
    Importer History Data Service Base Class
    """
    def __init__(self, import_history, importer, config):
        self.importer = importer

        self.import_history = import_history
        self._config = config

        if self._config.S3_ENABLED:
            self.s3 = S3Utility(self._config.AWS_ACCESS_KEY_ID,
                                self._config.AWS_SECRET_ACCESS_KEY,
                                self._config.AWS_RAW_IMPORT_DATA_BUCKET)

    @staticmethod
    def save(data):
        """
        Save data obj to DB
        :param data: dict
        :return: None
        """
        try:
            data.save()
        except NotUniqueError as e:
            logger.error(f"NotUniqueError: on '{data.key_name}' for code={data.data_object_id}")
            pass
        except Exception as e:
            logger.error(f"Error on saving {data.key_name} data: id={data.data_object_id} \n{str(e)}")

    def dump(self, data):
        """
        Create a dump of the data obj by dumping on local folder then upload the data folder to S3
        :param data:
        :return:
        """
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


class BaseDbService:

    def __init__(self, import_history_service):
        self.service = import_history_service

    def save(self, data_dict):
        obj = self.create_import_history_data(data_dict)
        self.service.save(obj)
        self.service.dump(obj)

    def save_all(self, data_dict_list):
        for data_dict in data_dict_list:
            obj = self.create_import_history_data(data_dict)
            self.service.save(obj)
            self.service.dump(obj)

    def save_bulk(self, data_dict_list):
        list_ = []
        for data_dict in data_dict_list:
            obj = self.create_import_history_data(data_dict)
            list_.append(obj)
            self.service.dump(obj)
        self.service.save_bulk(list_)

    @abstractmethod
    def create_import_history_data(self, data_dict):
        raise NotImplementedError
