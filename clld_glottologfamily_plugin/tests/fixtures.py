from sqlalchemy import Column, Integer, ForeignKey, Unicode

from clld.db.models.common import Language
from clld.db.meta import CustomModelMixin
from clld.web.datatables.language import Languages

from clld_glottologfamily_plugin.models import HasFamilyMixin
from clld_glottologfamily_plugin.datatables import MacroareaCol, FamilyLinkCol


class LanguageWithFamily(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    macroarea = Column(Unicode)


class LanguagesWithFamily(Languages):
    def col_defs(self):
        return [
            MacroareaCol(self, 'ma', language_cls=LanguageWithFamily),
            FamilyLinkCol(self, 'f', language_cls=LanguageWithFamily),
        ]
