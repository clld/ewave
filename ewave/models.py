from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Unicode,
    Integer,
    Float,
    Boolean,
    ForeignKey,
    UniqueConstraint,
)
from sqlalchemy.orm import relationship, backref
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.ext.hybrid import hybrid_property

from clld import interfaces
from clld.util import DeclEnum
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, Language, Contribution, IdNameDescriptionMixin,
)


class VarietyType(Base, IdNameDescriptionMixin):
    pass


class Region(Base, IdNameDescriptionMixin):
    pass


class FeatureCategory(Base, IdNameDescriptionMixin):
    pass


#-----------------------------------------------------------------------------
# specialized common mapper classes
#-----------------------------------------------------------------------------
@implementer(interfaces.ILanguage)
class Variety(Language, CustomModelMixin):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    region_pk = Column(Integer, ForeignKey('region.pk'))
    type_pk = Column(Integer, ForeignKey('varietytype.pk'))
    abbr = Column(String)

    region = relationship(Region, backref='varieties')
    type = relationship(VarietyType, backref='varieties')


@implementer(interfaces.IContribution)
class WaveContribution(Contribution, CustomModelMixin):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    variety_pk = Column(Integer, ForeignKey('variety.pk'))
    variety = relationship(Variety, backref=backref('contribution', uselist=False))


@implementer(interfaces.IParameter)
class Feature(Parameter, CustomModelMixin):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    category_pk = Column(Integer, ForeignKey('featurecategory.pk'))
    category = relationship(FeatureCategory, backref=backref('features'))
    attestation = Column(Float)
    pervasiveness = Column(Float)
