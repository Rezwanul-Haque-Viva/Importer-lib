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

    def set_response(self,
                     success: bool = None,
                     msg: str = None,
                     import_history_id: str = None,
                     importer_id: str = None):
        if success:
            self.EVENT_RESPONSE['success'] = success
        if msg:
            self.EVENT_RESPONSE['msg'] = msg
        if import_history_id:
            self.EVENT_RESPONSE['import_history_id'] = import_history_id
        if importer_id:
            self.EVENT_RESPONSE['importer_id'] = importer_id

    @property
    def get_response(self):
        return self.EVENT_RESPONSE
