from django.test.runner import DiscoverRunner
from django.db import connections

 
class MyDiscoverRunner(DiscoverRunner): 

    def setup_databases(self, *a, **kw): 
        ret = super(MyDiscoverRunner, self).setup_databases(*a, **kw) 
        cursor = connections['legacy'].cursor() 
        cursor.executescript(open('hawk_rest_api/legacy.sqlite3.sql').read())
        return ret
