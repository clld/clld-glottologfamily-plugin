"""Column implementations for DataTables."""
from sqlalchemy import null

from clld.db.meta import DBSession
from clld.db.util import icontains, get_distinct_values
from clld.web.datatables.base import Col, DataTable, LinkCol, IdCol
from clld.web.util.htmllib import HTML
from clld.web.util.helpers import map_marker_img, link, external_link
from clld_glottologfamily_plugin.models import Family


class MacroareaCol(Col):
    """Column displaying the macroarea assigned to a language."""

    def __init__(self, dt, name, language_cls, **kw):  # noqa: D107
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
    """Column displaying the family."""

    def __init__(self, dt, name, language_cls, link=False, **kw):  # noqa: D107
        self._link = link
        self._col = getattr(language_cls, 'family')
        kw['choices'] = [
            (f.id, f.name) for f in
            DBSession.query(Family).order_by(Family.name)]  # pylint: disable=E1101
        kw['choices'].insert(0, ('isolate', '--none--'))
        Col.__init__(self, dt, name, **kw)

    def order(self):  # pylint: disable=C0116
        return Family.name

    def search(self, qs):  # pylint: disable=C0116
        if qs == 'isolate':
            return self._col == null()
        return Family.id == qs

    def format(self, item):  # pylint: disable=C0116
        item = self.get_obj(item)
        if item.family:
            label = link(self.dt.req, item.family) if self._link else item.family.name
        else:
            label = 'isolate'
        return HTML.div(map_marker_img(self.dt.req, item), ' ', label)


class FamilyLinkCol(FamilyCol):
    """Column displaying a family as link to the family page."""

    def __init__(self, dt, name, language_cls, **kw):  # noqa: D107
        FamilyCol.__init__(self, dt, name, language_cls, link=True, **kw)


class GlottologUrlCol(Col):
    """Column displaying a Glottocode as link to Glottolog."""

    def format(self, item):  # pylint: disable=C0116
        return external_link(item.description, label=item.id)


class Familys(DataTable):
    """DataTable listing families."""

    def col_defs(self):  # pylint: disable=C0116
        return [
            IdCol(self, 'id'),
            LinkCol(self, 'name'),
            GlottologUrlCol(self, 'description', sTitle='Glottolog'),
        ]
