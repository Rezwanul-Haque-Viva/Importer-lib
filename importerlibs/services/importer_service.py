import logging

from mongoengine import DoesNotExist
from mongoengine.base.metaclasses import TopLevelDocumentMetaclass

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class ImporterService:
    def __init__(self, config: TopLevelDocumentMetaclass):
        self._importer_config = config

    def get_importer_config(self, importer_id: str) -> object:
        try:
            importer_obj = self._importer_config.objects(id=importer_id).get()
            return importer_obj
        except DoesNotExist as e:
            raise e
        except Exception as e:
            raise e

    def update_importer_status(self, importer_id: str, importer_status: str, imp_execution_status: str) -> None:
        try:
            importer_obj = self.get_importer_config(importer_id=importer_id)
            importer_obj.status = importer_status
            importer_obj.execution_status = imp_execution_status
            importer_obj.save()
        except Exception as error:
            raise error

    def update_importer_last_history_id(self, importer_id: str, import_history_id: str) -> None:
        try:
            importer_obj = self.get_importer_config(importer_id=importer_id)
            importer_obj.last_import_history = import_history_id
            importer_obj.save()
        except Exception as error:
            raise error
