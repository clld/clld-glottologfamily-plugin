from __future__ import unicode_literals

from pyramid.testing import Configurator
from mock import MagicMock

from clld.scripts.util import Data
from clld.tests.util import TestWithDb, ExtendedTestApp
from clld.db.meta import DBSession
from clld.db.models import common

from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.tests.fixtures import (
    LanguageWithFamily, LanguagesWithFamily,
)


class _TestWithDb(TestWithDb):
    __with_custom_language__ = False

    def setUp(self):
        TestWithDb.setUp(self)
        DBSession.add(common.Dataset(id='d', name='test', domain='localhost'))
        family = Family(id='f', name='family', description='desc', jsondata=dict(icon=1))
        DBSession.add(LanguageWithFamily(id='l1', family=family))
        DBSession.add(LanguageWithFamily(id='l2'))
        DBSession.flush()


class TestWithApp(_TestWithDb):
    def setUp(self):
        _TestWithDb.setUp(self)
        config = Configurator(settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': ['clld:web/templates']})
        config.include('clld.web.app')
        config.include('clld_glottologfamily_plugin')
        config.register_datatable('languages', LanguagesWithFamily)
        self.app = ExtendedTestApp(config.make_wsgi_app())

    def test_templates(self):
        self.app.get_html('/familys')
        self.app.get_dt('/familys')
        self.app.get_html('/familys/f')
        self.app.get_json('/familys/f.json')
        self.app.get_xml('/familys/f.rdf')

    def test_datatables(self):
        self.app.get_html('/languages')
        self.app.get_dt('/languages')
        self.app.get_dt('/languages?sSearch_0=m&sSearch_1=n&iSortingCols=1&iSortCol_0=0')


class Tests(_TestWithDb):
    def test_Family(self):
        assert DBSession.query(Family).first().url == 'desc'

    def test_FamilyCol(self):
        from clld_glottologfamily_plugin.datatables import FamilyCol

        col = FamilyCol(MagicMock(), 'family', language_cls=LanguageWithFamily)
        q = DBSession.query(LanguageWithFamily).outerjoin(Family)
        assert q.filter(col.search('isolate')).all()
        assert q.filter(col.search('f')).order_by(col.order()).all()

    def test_load_families(self):
        from clld_glottologfamily_plugin.util import load_families

        class Languoid(object):
            id = 'abcd1234'
            iso_code = 'abc'
            name = 'language'
            latitude = 1.0
            longitude = 1.0
            macroareas = ['Area']

            @property
            def family(self):
                return self

        class TopLevelFamily(object):
            id = 'abcd1234'
            iso_code = 'abc'
            name = 'family'
            latitude = 1.0
            longitude = 1.0
            macroareas = ['Area']
            level = 'family'

            @property
            def family(self):
                return None

        class Glottolog(object):
            def languoid(self, code):
                if code == 'abc':
                    return TopLevelFamily()
                return Languoid()

        load_families(Data(), DBSession.query(LanguageWithFamily), glottolog=Glottolog())
        load_families(
            Data(),
            [('abc', l) for l in DBSession.query(LanguageWithFamily)],
            glottolog=Glottolog())

    def test_LanguageByFamilyMapMarker(self):
        from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

        marker = LanguageByFamilyMapMarker()
        self.assertEqual(marker.get_icon(LanguageWithFamily.get('l1'), MagicMock()), 1)
        self.assertNotEqual(marker.get_icon(LanguageWithFamily.get('l2'), MagicMock()), 1)
        marker.get_icon(Family.first(), MagicMock())

    def test_includeme(self):
        config = Configurator(settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': []})
        config.include('clld.web.app')
        config.include('clld_glottologfamily_plugin')
