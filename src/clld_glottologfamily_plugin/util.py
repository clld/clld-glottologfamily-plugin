"""Utilities to load Glottolog data etc."""
import pathlib
import itertools
from collections.abc import Iterable, Sequence

from clld.web.icon import ORDERED_ICONS, MapMarker
from clld.cliutil import add_language_codes, Data
from clld.web.icon import Icon
from clld.interfaces import ILanguage
from clld.db.models.common import IdentifierType, Identifier, Language

try:
    from pyglottolog.api import Glottolog
except ImportError:  # pragma: no cover
    Glottolog = None

from clld_glottologfamily_plugin.models import Family


ISOLATES_ICON = 'cff6600'


class LanguageByFamilyMapMarker(MapMarker):
    def get_icon(self, ctx, req):
        if ILanguage.providedBy(ctx):  # pylint: disable=E1120
            if ctx.family:
                return ctx.family.jsondata['icon']
            return req.registry.settings.get('clld.isolates_icon', ISOLATES_ICON)
        return super().get_icon(ctx, req)


def load_families(data: Data,  # pylint: disable=R0913,R0917
                  languages: Iterable[tuple[str, Language] | Language],
                  glottolog_repos: pathlib.Path | None = None,
                  strict: bool = True,
                  icons: Sequence[Icon] = ORDERED_ICONS,
                  isolates_icon: str = ISOLATES_ICON):
    """Add Family objects to a database and update Language object from Glottolog.

    Family information is retrieved from Glottolog based on the id attribute of a
    language. This id must be either a glottocode or an ISO 639-3 code.
    """
    def copy_attrs(from_, to_, *attrs: str):
        for attr in attrs:
            if getattr(to_, attr) is None:
                setattr(to_, attr, getattr(from_, attr))

    if Glottolog is None:
        raise ImportError('Package must be installed with [initdb] extra.')  # pragma: no cover
    api = Glottolog(glottolog_repos)
    icons = itertools.cycle(
        [getattr(i, 'name', i) for i in icons if getattr(i, 'name', i) != isolates_icon])
    languoids_by_code = api.languoids_by_code()
    for language in languages:
        if isinstance(language, tuple):
            assert len(language) == 2 and isinstance(language[0], str)
            code, language = language
        else:
            code = language.id
        gl_language = languoids_by_code.get(code)
        if strict and not gl_language:
            raise KeyError(code)
        gl_family = None
        if gl_language:
            if not gl_language.lineage:
                if gl_language.level.id == api.languoid_levels.family.id:
                    # Make sure top-level families are not treated as isolates!
                    gl_family = gl_language
            else:
                gl_family = languoids_by_code[gl_language.lineage[0][1]]
            language.macroarea = \
                gl_language.macroareas[0].name if gl_language.macroareas else None
            add_language_codes(
                data, language, gl_language.iso, glottocode=gl_language.id)
            copy_attrs(gl_language, language, 'latitude', 'longitude', 'name')

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
                    jsondata={'icon': next(icons)})
            language.family = family
