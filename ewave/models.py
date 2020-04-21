from zope.interface import implementer
from sqlalchemy import (
    Column,
    String,
    Integer,
    Float,
    ForeignKey,
    Unicode,
)
from sqlalchemy.orm import relationship, backref

from clld import interfaces
from clld.db.meta import Base, CustomModelMixin
from clld.db.models.common import (
    Parameter, Language, Contribution, IdNameDescriptionMixin, Contributor,
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
class Variety(CustomModelMixin, Language):
    pk = Column(Integer, ForeignKey('language.pk'), primary_key=True)
    region_pk = Column(Integer, ForeignKey('region.pk'))
    type_pk = Column(Integer, ForeignKey('varietytype.pk'))
    abbr = Column(String)

    region = relationship(Region, backref='varieties')
    type = relationship(VarietyType, backref='varieties')

    @property
    def glottocode(self):
        if self.languageidentifier:
            return self.languageidentifier[0].identifier.name

    def __json__(self, req):
        res = super(Variety, self).__json__(req)
        res['type'] = {'name': self.type.name, 'pk': self.type.pk}
        return res


@implementer(interfaces.IContributor)
class WaveContributor(CustomModelMixin, Contributor):
    pk = Column(Integer, ForeignKey('contributor.pk'), primary_key=True)
    sortkey = Column(Unicode)


@implementer(interfaces.IContribution)
class WaveContribution(CustomModelMixin, Contribution):
    pk = Column(Integer, ForeignKey('contribution.pk'), primary_key=True)
    variety_pk = Column(Integer, ForeignKey('variety.pk'))
    variety = relationship(Variety, backref=backref('contribution', uselist=False))


@implementer(interfaces.IParameter)
class Feature(CustomModelMixin, Parameter):
    pk = Column(Integer, ForeignKey('parameter.pk'), primary_key=True)
    category_pk = Column(Integer, ForeignKey('featurecategory.pk'))
    category = relationship(FeatureCategory, backref=backref('features'))
    attestation = Column(Float)
    pervasiveness = Column(Float)
