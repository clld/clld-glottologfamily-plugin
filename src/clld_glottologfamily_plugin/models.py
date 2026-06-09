"""
Schema objects for the plugin.
"""
from zope.interface import implementer
from sqlalchemy import (
    Column,
    Unicode,
    Integer,
    ForeignKey,
)
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declared_attr

from clld.db.meta import Base
from clld.db.models.common import IdNameDescriptionMixin

from clld_glottologfamily_plugin.interfaces import IFamily


@implementer(IFamily)
class Family(Base, IdNameDescriptionMixin):
    """A Family table."""
    @property
    def url(self):  # pylint: disable=C0116
        return self.description


class HasFamilyMixin:
    """Adds a family relationship."""
    macroarea = Column(Unicode)

    @declared_attr
    def family_pk(cls):  # pylint: disable=E0213,C0116
        return Column(Integer, ForeignKey('family.pk'))

    @declared_attr
    def family(cls):  # pylint: disable=E0213,C0116
        return relationship(Family, backref='languages')
