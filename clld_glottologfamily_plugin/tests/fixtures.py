from sqlalchemy import Column, Integer, ForeignKey

from clld.db.models.common import Language
from clld.db.meta import CustomModelMixin

from clld_glottologfamily_plugin.models import HasFamilyMixin


class LanguageWithFamily(CustomModelMixin, Language, HasFamilyMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
