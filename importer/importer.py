from abc import ABCMeta, abstractmethod


class ImporterBaseClass(metaclass=ABCMeta):

    @abstractmethod
    def load_importer_data(self):
        raise NotImplementedError
