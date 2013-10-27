import mercy.db

class FDAImporter:
    def __init__(self, *args, **kwargs):
        self.__database = mercy.db.Database()

    def read(self, fname):
        raise Exception("FDAImporter.read doesn't do anything yet")
