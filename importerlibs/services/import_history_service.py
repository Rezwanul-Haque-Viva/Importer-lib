from datetime import datetime

from models.history.import_history import ImportHistory
from mongoengine import DoesNotExist


def create_import_history(importer: object) -> object:
    try:
        import_history = ImportHistory(
            importer_name=importer.name,
            base_url='',
            importer_start_time=datetime.utcnow(),
            importer_config=importer.id,
            importer_config_sanpshot=importer.to_mongo()
        )
        import_history.save()
        return import_history

    except Exception as e:
        raise e


def get_import_history(import_history_id: str) -> object:
    try:
        import_history_obj = ImportHistory.objects(id=import_history_id).get()
        return import_history_obj
    except DoesNotExist as e:
        raise e
    except Exception as e:
        raise e


def update_error(import_history_id: str, error_msg: str) -> object:
    try:
        importer_history_obj = ImportHistory.objects(id=import_history_id).get()
        importer_history_obj.error = {'msg': error_msg}
        importer_history_obj.save()
        return importer_history_obj
    except DoesNotExist as e:
        raise e
    except Exception as e:
        raise e


def update_importer_stats(import_history_id: str, stats: dict):
    try:
        importer_history_obj = ImportHistory.objects(id=import_history_id).get()
        importer_history_obj.stats['importer_count'] = stats
        importer_history_obj.save()
        return importer_history_obj
    except DoesNotExist as e:
        raise e
    except Exception as e:
        raise e
