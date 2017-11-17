from __future__ import unicode_literals

from pyglottolog.objects import Macroarea, Level
from clld.scripts.util import Data
from clld.db.meta import DBSession
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.datatables import FamilyCol

import pytest


@pytest.mark.parametrize(
    "method,url,content",
    [
        ('html', '/familys', '<h2>Families'),
        ('dt', '/familys', None),
        ('html', '/familys/f', '<h2>Family'),
        ('json', '/familys/f.json', None),
        ('xml', '/familys/f.rdf', None),
        ('html', '/languages', None),
        ('dt', '/languages', None),
        ('dt', '/languages?sSearch_0=m&sSearch_1=n&iSortingCols=1&iSortCol_0=0', None),
    ])
def test_url(testapp, method, url, content):
    res = getattr(testapp, 'get_' + method)(url)
    if content:
        assert content in res.body.decode('utf8')


def test_Family(engine, db):
    assert DBSession.query(Family).first().url == 'desc'


def test_FamilyCol(engine, db, mocker, language_with_family):
    col = FamilyCol(mocker.MagicMock(), 'family', language_cls=language_with_family)
    q = DBSession.query(language_with_family).outerjoin(Family)
    assert q.filter(col.search('isolate')).all()
    assert q.filter(col.search('f')).order_by(col.order()).all()


def test_load_families(mocker, engine, db, language_with_family):
    from clld_glottologfamily_plugin.util import load_families

    class _L(object):
        latitude = 1.0
        longitude = 1.0
        macroareas = [Macroarea.pacific]

    class Isolate(_L):
        id = 'abcd1236'
        name = 'isolate'
        iso = None
        level = Level.language
        lineage = []

    class Languoid(_L):
        id = 'abcd1235'
        iso = 'abc'
        name = 'language'
        lineage = [('n', 'abcd1234', '')]

    class TopLevelFamily(_L):
        id = 'abcd1234'
        iso = 'abc'
        name = 'family'
        level = Level.family
        lineage = []

    class Glottolog(mocker.Mock):
        def languoids_by_code(self):
            return dict(
                l1=Languoid(),
                abcd1236=Isolate(),
                abcd1234=TopLevelFamily(),
                abc=TopLevelFamily())

    mocker.patch('clld_glottologfamily_plugin.util.Glottolog', Glottolog)
    load_families(Data(), DBSession.query(language_with_family), strict=False)
    load_families(
        Data(),
        [('abc', l) for l in DBSession.query(language_with_family)],
        strict=False)


def test_load_families2(mocker, engine, db, language_with_family):
    from clld_glottologfamily_plugin.util import load_families

    class Glottolog(mocker.Mock):
        def languoids_by_code(self):
            return {}

    mocker.patch('clld_glottologfamily_plugin.util.Glottolog', Glottolog)
    with pytest.raises(KeyError):
        load_families(Data(), DBSession.query(language_with_family))


def test_LanguageByFamilyMapMarker(engine, db, mocker, language_with_family):
    from clld_glottologfamily_plugin.util import LanguageByFamilyMapMarker

    marker = LanguageByFamilyMapMarker()
    assert marker.get_icon(language_with_family.get('l1'), mocker.MagicMock()) == 1
    assert marker.get_icon(language_with_family.get('l2'), mocker.MagicMock()) != 1
    marker.get_icon(Family.first(), mocker.MagicMock())


def test_includeme():
    from pyramid.testing import Configurator

    config = Configurator(settings={
        'sqlalchemy.url': 'sqlite://',
        'mako.directories': []})
    config.include('clld.web.app')
    config.include('clld_glottologfamily_plugin')
