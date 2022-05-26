from databases import Database


class BaseRepository:

    def __init__(self, database: Database):
        self._database = database
