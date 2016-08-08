import sys


class MyDatabaseRouter(object):

    def _db_for_all(self, model, **hints):
        if model._meta.managed is False:
            return 'legacy'
        return None

    def db_for_read(self, model, **hints):
        return self._db_for_all(model, **hints)

    def db_for_write(self, model, **hints):
        return self._db_for_all(model, **hints)

    def allow_migrate(self, db, app_label, **hints):
        if db == 'legacy':
            return False
        return None
