import pathlib

import sqlalchemy as sa
from pyramid import config
import pytest

from clld.db.meta import DBSession, Base, CustomModelMixin
from clld.db.models import common
from clld.web.datatables.language import Languages
from pytest_clld._app import ExtendedTestApp
from clld_glottologfamily_plugin.models import Family, HasFamilyMixin
from clld_glottologfamily_plugin.datatables import MacroareaCol, FamilyLinkCol


@pytest.fixture()
def glottolog_repos():
    return pathlib.Path(__file__).parent / 'repos'


class LanguageWithFamily(CustomModelMixin, common.Language, HasFamilyMixin):
    pk = sa.Column(sa.Integer, sa.ForeignKey('language.pk'), primary_key=True)
    macroarea = sa.Column(sa.Unicode)


@pytest.fixture(scope='session')
def language_with_family():
    return LanguageWithFamily


class LanguagesWithFamily(Languages):
    def col_defs(self):
        return [
            MacroareaCol(self, 'ma', language_cls=LanguageWithFamily),
            FamilyLinkCol(self, 'f', language_cls=LanguageWithFamily),
        ]


@pytest.fixture
def engine():
    DBSession.bind = sa.create_engine('sqlite://')
    yield DBSession
    DBSession.remove()


@pytest.fixture
def db():
    Base.metadata.bind = DBSession.bind
    Base.metadata.create_all()

    DBSession.add(common.Dataset(id='1', name='test app', domain='example.org'))
    family = Family(id='f', name='family', description='desc', jsondata=dict(icon=1))
    DBSession.add(LanguageWithFamily(id='l1', family=family))
    DBSession.add(LanguageWithFamily(id='l2'))
    DBSession.add(LanguageWithFamily(id='abcd1236'))
    DBSession.add(LanguageWithFamily(id='abcd1234'))
    return DBSession


@pytest.fixture(scope='module')
def testapp():
    def main():
        cfg = config.Configurator(settings={
            'sqlalchemy.url': 'sqlite://',
            'mako.directories': [
                'clld:web/templates',
                'clld_glottologfamily_plugin:templates'
            ]})
        cfg.include('clld.web.app')
        cfg.include('clld_glottologfamily_plugin')
        cfg.register_datatable('languages', LanguagesWithFamily)
        return cfg.make_wsgi_app()

    DBSession.remove()
    wsgi_app = main()
    Base.metadata.bind = DBSession.bind
    Base.metadata.create_all()

    DBSession.add(common.Dataset(id='1', name='test app', domain='example.org'))
    family = Family(id='f', name='family', description='desc', jsondata=dict(icon=1))
    DBSession.add(LanguageWithFamily(id='l1', family=family))
    DBSession.add(LanguageWithFamily(id='l2'))
    DBSession.add(LanguageWithFamily(id='abcd1236'))
    yield ExtendedTestApp(wsgi_app)
