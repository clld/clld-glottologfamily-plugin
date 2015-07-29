from __future__ import unicode_literals

from clld.web.adapters.base import Representation, Index
from clld.web.adapters.rdf import Rdf, RdfIndex
from clld.web.adapters.geojson import GeoJson
from clld.web.maps import Map
from clld.lib.rdf import FORMATS
from clld_glottologfamily_plugin.models import Family
from clld_glottologfamily_plugin.interfaces import IFamily
from clld_glottologfamily_plugin.datatables import Familys


def includeme(config):
    config.register_resource('family', Family, IFamily, with_index=True)
    config.registry.settings['mako.directories'].append(
        'clld_glottologfamily_plugin:templates')

    specs = [
        [Representation, 'text/html', 'html', 'family/detail_html.mako', {}],
        [Index, 'text/html', 'html', 'family/index_html.mako', {}],
        [RdfIndex, FORMATS['xml'].mimetype, FORMATS['xml'].extension, 'index_rdf.mako',
         {'rdflibname': FORMATS['xml'].name}]
    ]
    for fmt in FORMATS.values():
        specs.append([
            Rdf,
            fmt.mimetype,
            fmt.extension,
            'family/rdf.mako',
            {'name': 'RDF serialized as %s' % fmt.name, 'rdflibname': fmt.name}])
    config.register_adapters([[IFamily] + spec for spec in specs])
    config.register_adapter(GeoJson, IFamily)
    config.register_map('family', Map)
    config.register_datatable('familys', Familys)
