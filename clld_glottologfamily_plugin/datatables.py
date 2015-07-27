from sqlalchemy import null

from clld.db.meta import DBSession
from clld.db.util import icontains, get_distinct_values
from clld.web.datatables.base import Col
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import map_marker_img
from clld_glottologfamily_plugin.models import Family


class MacroareaCol(Col):
    def __init__(self, dt, name, language_cls, **kw):
        self._col = getattr(language_cls, 'macroarea')
        kw['choices'] = get_distinct_values(self._col)
        self.language_cls = language_cls
        Col.__init__(self, dt, name, **kw)

    def order(self):
        return self._col

    def search(self, qs):
        return icontains(self._col, qs)

    def format(self, item):
        return self.get_obj(item).macroarea


class FamilyCol(Col):
    def __init__(self, dt, name, language_cls, **kw):
        self._col = getattr(language_cls, 'family')
        kw['choices'] = [
            (f.id, f.name) for f in DBSession.query(Family).order_by(Family.name)]
        kw['choices'].insert(0, ('isolate', '--none--'))
        Col.__init__(self, dt, name, **kw)

    def order(self):
        return Family.name

    def search(self, qs):
        if qs == 'isolate':
            return self._col == null()
        return Family.id == qs

    def format(self, item):
        item = self.get_obj(item)
        label = item.family.name if item.family else 'isolate'
        return HTML.div(map_marker_img(self.dt.req, item), ' ', label)
