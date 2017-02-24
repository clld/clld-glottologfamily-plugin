from __future__ import unicode_literals
from itertools import cycle

from six import next

from clld.web.icon import ORDERED_ICONS, MapMarker
from clld.scripts.util import add_language_codes
from clld.interfaces import ILanguage
from clld.db.models.common import IdentifierType, Identifier

from pyglottolog.api import Glottolog
from pyglottolog.objects import Level

from clld_glottologfamily_plugin.models import Family


ISOLATES_ICON = 'cff6600'


class LanguageByFamilyMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if ILanguage.providedBy(ctx):
            if ctx.family:
                return ctx.family.jsondata['icon']
            return req.registry.settings.get('clld.isolates_icon', ISOLATES_ICON)
        return super(LanguageByFamilyMapMarker, self).get_icon(ctx, req)


def load_families(data,
                  languages,
                  glottolog_repos=None,
                  icons=ORDERED_ICONS,
                  isolates_icon=ISOLATES_ICON):
    """Add Family objects to a database and update Language object from Glottolog.

    Family information is retrieved from Glottolog based on the id attribute of a
    language. This id must be either a glottocode or an ISO 639-3 code.

    :param data:
    :return:
    """
    icons = cycle([getattr(i, 'name', i) for i in icons
                   if getattr(i, 'name', i) != isolates_icon])
    languoids_by_code = Glottolog(glottolog_repos).languoids_by_code()
    for language in languages:
        if isinstance(language, (tuple, list)) and len(language) == 2:
            code, language = language
        else:
            code = language.id
        gl_language = languoids_by_code.get(code)
        if gl_language:
            if not gl_language.lineage:
                if gl_language.level == Level.family:
                    # Make sure top-level families are not treated as isolates!
                    gl_family = gl_language
                else:
                    gl_family = None
            else:
                gl_family = languoids_by_code[gl_language.lineage[0][1]]

            if gl_family:
                family = data['Family'].get(gl_family.id)
                if not family:
                    family = data.add(
                        Family,
                        gl_family.id,
                        id=gl_family.id,
                        name=gl_family.name,
                        description=Identifier(
                            name=gl_family.id, type=IdentifierType.glottolog.value).url(),
                        jsondata=dict(icon=next(icons)))
                language.family = family

            language.macroarea = \
                gl_language.macroareas[0].value if gl_language.macroareas else None
            add_language_codes(
                data, language, gl_language.iso, glottocode=gl_language.id)
            for attr in 'latitude', 'longitude', 'name':
                if getattr(language, attr) is None:
                    setattr(language, attr, getattr(gl_language, attr))
