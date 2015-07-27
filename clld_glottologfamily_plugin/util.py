from __future__ import unicode_literals
from itertools import cycle

from clld.web.icon import ORDERED_ICONS, MapMarker
from clld.scripts.util import add_language_codes
from clld.interfaces import ILanguage

from clldclient.glottolog import Glottolog

from clld_glottologfamily_plugin.models import Family


ISOLATES_ICON = 'cff6600'


class LanguageByFamilyMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if ILanguage.providedBy(ctx):
            if ctx.family:
                return ctx.family.jsondata['icon']
            return ISOLATES_ICON
        return super(LanguageByFamilyMapMarker, self).get_icon(ctx, req)


def load_families(data, languages):
    """Add Family objects to a database and update Language object from Glottolog.

    Family information is retrieved from Glottolog based on the id attribute of a
    language. This id must be either a glottocode or an ISO 639-3 code.

    :param data:
    :return:
    """
    icons = cycle([i for i in ORDERED_ICONS if i.name != ISOLATES_ICON])
    glottolog = Glottolog()

    for language in languages:
        gl_language = glottolog.languoid(language.id)
        if gl_language:
            gl_family = gl_language.get_family(glottolog)
            if gl_family:
                family = data['Family'].get(gl_family.id)
                if not family:
                    family = data.add(
                        Family,
                        gl_family.id,
                        id=gl_family.id,
                        name=gl_family.name,
                        description='',
                        jsondata=dict(icon=icons.next().name))
                language.family = family
            language.macroarea = gl_language['macroareas'].values()[0]
            add_language_codes(
                data, language, gl_language.get('iso639-3'), glottocode=gl_language.id)
            for attr in 'latitude', 'longitude', 'name':
                if not getattr(language, attr) and gl_language.get('attr') is not None:
                    setattr(language, attr, gl_language[attr])
