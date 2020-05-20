import logging

log = logging.getLogger(__name__)
log.setLevel(logging.INFO)
current_user = None


class ResponseManager:
    EVENT_RESPONSE = {
        "success": False,
        "importer_id": None,
        "import_history_id": None,
        "msg": "Importer not yet started"
    }

    @classmethod
    def set_response(cls,
                     success: bool = None,
                     msg: str = None,
                     import_history_id: str = None,
                     importer_id: str = None):
        if success:
            cls.EVENT_RESPONSE['success'] = success
        if msg:
            cls.EVENT_RESPONSE['msg'] = msg
        if import_history_id:
            cls.EVENT_RESPONSE['import_history_id'] = import_history_id
        if importer_id:
            cls.EVENT_RESPONSE['importer_id'] = importer_id

    @classmethod
    def get_response(cls):
        return cls.EVENT_RESPONSE
