import logging
import mwparserfromhell as mwp

from wikitables.client import Client
from wikitables.models import WikiTable, ftag

logging.basicConfig(level=logging.WARN)
log = logging.getLogger('wikitables')

def import_tables(article):
    client = Client()
    page = client.fetch_page(article)
    body = page['revisions'][0]['*']

    ## parse for tables
    raw_tables = mwp.parse(body).filter_tags(matches=ftag('table'))

    def _table_gen():
        for idx, table in enumerate(raw_tables):
            name = '%s[%s]' % (page['title'],idx)
            yield WikiTable(name, table)

    return list(_table_gen())
