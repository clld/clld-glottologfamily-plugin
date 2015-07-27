from mock import MagicMock

from clld.tests.util import TestWithDb
from clld.db.meta import DBSession

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.tests.fixtures import LanguageWithFamily


class Tests(TestWithDb):
    def setUp(self):
        TestWithDb.setUp(self)
        family = Family(id='f', name='family', description='desc')
        DBSession.add(LanguageWithFamily(id='l1', family=family))
        DBSession.add(LanguageWithFamily(id='l2'))
        DBSession.flush()

    def test_Family(self):
        assert DBSession.query(Family).first().url == 'desc'

    def test_FamilyCol(self):
        from clld_glottologfamily_plugin.datatables import FamilyCol

        col = FamilyCol(MagicMock(), 'family', language_cls=LanguageWithFamily)
        q = DBSession.query(LanguageWithFamily).outerjoin(Family)
        assert q.filter(col.search('isolate')).all()
        assert q.filter(col.search('f')).order_by(col.order()).all()
