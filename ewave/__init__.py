from functools import partial

from clld.web.app import get_configurator, menu_item
from clld.web.icon import MapMarker
from clld.web.maps import Map
from clld import interfaces

# we must make sure custom models are known at database initialization!
from ewave import models
from ewave.maps import LanguageMap
from ewave.datatables import WaveContributions, Features, Values
from ewave.adapters import GeoJsonContributions

"""
eWAVE Statistics

1. Feature statistics
(calculated for individual features across (a subset of) varieties)

1.1 Number of attestations
The number of attestations is an absolute measure of how widespread a feature is in a set of varieties. It is calculated as the sum of all A-, B- and C-ratings for the current feature in the currently selected set of varieties. Thus, the closer the number of attestations to the number of varieties in the selected set, the more widespread a feature is.
Formula:	A(fi,v)+B(fi,v)+C(fi,v)
Example:	Feature 91 (Do as habitual marker) is rated A in 5 of the 74 WAVE-varieties, B in 4, and C in 11. In the other 54 varieties, it is rated D, X or ?. Thus, the number of attestations for feature 91 across all 74 varieties in eWAVE is 5+4+11 = 20. If we consider only the traditional L1 varieties (L1t), however, feature 91 is attested rated A or B in none, and rated C in only 2 out of the 10 L1t varieties. Thus, for the subset of L1t varieties, the number of attestations is 0+0+2 = 2.

1.2 Attestation rate
The attestation rate is a relative measure of how widespread a feature is in a set of WAVE varieties. It is expressed as a percentage and is calculated as the number of attestations for a feature in a set of varieties, divided by the number of varieties in that set. The closer the value to 100%, the more widespread a feature. Features with an attestation rate of 75% or higher in a set of varieties can be considered top features of that set. Note, however, that the significance of attestation rate values decreases with sample size. That is, the lower the number of varieties in a subset, the less significant the attestation rate value. For instance, if the set that you are interested in consists of only 3 varieties, an attestation rate of 33% does not necessarily mean a lot, as it translates into a single attestation.
Formula:	[A(fi,v)+B(fi,v)+C(fi,v)]/v
Example:	Feature 91 (Do as habitual marker) is rated A in 5 of the 74 WAVE-varieties, B in 4, and C in 11. In the other 54 varieties, it is rated D, X or ?. Thus, the attestation rate of F91 across all WAVE varieties, is (5+4+11)/74 = 0.27 = 27%. If we consider the L1t varieties only, the value is (0+0+2)/10 = 0.20 = 20%.

1.3 Pervasiveness index (current feature in selected varieties)
The pervasiveness index (PI) provides a measure of how pervasive a feature is on average in the varieties in which it is attested. It is calculated as all A-ratings for a feature in the currently selected set of varieties, plus 0.6 times the B-ratings for the same feature in the same set, plus 0.3 times the C-ratings for that feature in that set, divided by the number of attestations for the feature in the relevant set of varieties. A value of 1 or close to 1 thus indicates that the feature is highly pervasive (rated A) in all or most of the varieties for which it is attested, while a value close to 0.3 indicates that the feature is extremely rare (rated C) in most or all of the varieties for which it is attested. Intermediate values are less easy to interpret, but the ratio of A- to B- to C-ratings can be inferred from the bar graph. Note that the PI value does not provide information on how widespread a feature is across the varieties in the selected subset, i.e. for how many varieties the feature is actually attested.
Formula: [A(fi,v) + 0.6*B(fi,v) + 0.3*C(fi,v)]/[A(fi,v)+B(fi,v)+C(fi,v)]
Example: Feature 91 (Do as habitual marker) is rated A in 5 of the 74 WAVE-varieties, B in 4, and C in 11. In the other 54 varieties, it is rated D, X or ?. Thus, the pervasiveness index for F91 across all 74 WAVE varieties is (5*1+4*0.6+11*0.3)/(5+4+11) = 10.7/20 = 0.535 For the set of L1t-varieties, however, the PI value of F91 is (0*1+0*0.6+2*0.3)/2 = 0.3.


2. Varieties statistics
(calculated for individual varieties across (a subset of) features)

2.1 Number of features attested
The number of features attested is a measure of how many of the WAVE-features - or of the currently selected subset of features - are attested in a given variety. It is calculated as the sum of all A-, B- and C- ratings for the relevant set of features in the selected variety. Since the WAVE-features are mostly non-standard features, a high value for this measure (close to the total number of features in the currently selected set) can be read as an indication of a high degree of distance of the relevant variety from Standard English.
Formula:	A(f,vj)+B(f,vj)+C(f,vj)
Example:	In Ghanaian Pidgin, 31of the 235 WAVE features are rated A, 20 are rated B and 9 are rated C. The rest are rated as either absent (D, 106), not applicable (X, 68), or there is no information available (?, 1). Thus, the number of attested features for Ghanaian Pidgin is 31+20+9 = 60. However, if we only consider the pronoun features in Ghanaian Pidgin, the number of attested features is 11 (7A+3B+1C = 11).

2.2 Proportion of features attested
The proportion of features attested is a measure of the share of (a given subset of) WAVE features that is attested in the selected variety. In analogy to the attestation rate, it is expressed as a percentage and is calculated as the sum of all A-, B- and C-ratings for the currently selected set of features in the given variety, divided by the total number of features in the selected set. In contrast to the absolute number of features attested, it permits direct comparisons across different subsets of features, e.g. in order to assess which feature groups in particular contribute to the 'standardness' or 'non-standardness' of a variety.
Formula:	[A(f,vj)+B(f,vj)+C(f,vj)]/f
Example:	For Ghanaian Pdigin, 60 attested features (31A+20B+9C) translate into a share of (31+20+9)/235 = 0.255 = 25.5% of all 235 WAVE features. Within the subset of pronoun features (which consists of features 1-47), the proportion of attested features is (7+3+1)/47= 0.234 = 23.4%

2.3 Pervasiveness index (selected features in current variety)
The pervasiveness index for a set of features in an individual variety provides a measure of how pervasive these features are on average in the given variety. It is calculated as the sum of all A-ratings for the selected set of features in the current variety + 0.6 times the number of B-ratings for the same set of features in the same variety + 0.3 times the number of C ratings for the same set of features in the same variety, divided by the number of all A-, B- and C- ratings for the selected set of features in the given variety. A value of 1 or close to 1 thus indicates that most of the features attested for the current variety are rated 'pervasive' (A), while a value of 0.3 or close to 0.3 indicates that most of the features that are attested are rare (rated C). Intermediate values are less easy to interpret, but the ratio of A- to B- to C-ratings can be inferred from the bar graph.
Formula:	[A(f,vj)+0.6*B(f,vj)+0.3*C(f,vj)]/[A(f,vj)+B(f,vj)+C(f,vj)]
Example:	For Ghanaian Pidgin, with 31 features rated A, 20 rated B, and 9 rated C, the pervasiveness index calculated over all 60 attested features is (31*1+20*0.6+9*0.3)/(31+20+9) = 0.762. The pervasiveness index calculated over the group of pronoun features in Ghanaian Pidgin (7A, 3B, 1C) is (7*1+3*0.6+1*0.3)/(7+3+1) = 0.827.

Key to abbreviations:
v = number of varieties in currently selected subset
A(fi, v) = number of varieties in currently selected subset which are rated A for feature i (analogously for other ratings)
f = number of features in currently selected subset
A(f,vj) = number of features in currently selected subset which are rated A in variety j (analogously for other ratings)
"""

_ = lambda s: s
_('Sentences')
_('Parameters')
_('Languages')
_('Sentence')
_('Parameter')
_('Language')
_('Contributors')
_('Contributor')
_('Contributions')
_('Contribution')


class WaveMapMarker(MapMarker):
    def __call__(self, ctx, req):
        icon = None

        if interfaces.ILanguage.providedBy(ctx):
            icon = ctx.type.jsondata['shape'] + ctx.type.jsondata['color']

        if interfaces.IContribution.providedBy(ctx):
            return self.__call__(ctx.variety, req)

        if interfaces.IValueSet.providedBy(ctx):
            icon = ctx.language.type.jsondata['shape'] + ctx.jsondata['color']

        if interfaces.IValue.providedBy(ctx):
            return self.__call__(ctx.valueset, req)

        if interfaces.IDomainElement.providedBy(ctx):
            icon = 'c' + ctx.jsondata['color']

        if icon:
            return req.registry.getUtility(interfaces.IIcon, icon).url(req)

        return super(WaveMapMarker, self).__call__(ctx, req)


def link_attrs(req, obj, **kw):
    if interfaces.ILanguage.providedBy(obj):
        # we are about to link to a language details page: redirect to contribution page!
        kw['href'] = req.route_url('contribution', id=obj.id, **kw.pop('url_kw', {}))
    if interfaces.IParameter.providedBy(obj):
        # we are about to link to a language details page: redirect to contribution page!
        kw['label'] = '%s %s' % (obj.id, obj.name)
    if interfaces.IValueSet.providedBy(obj):
        kw['title'] = obj.values[0].domainelement.description
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['sitemaps'] = 'contribution parameter sentence valueset'.split()
    utilities = [
        (WaveMapMarker(), interfaces.IMapMarker),
        (link_attrs, interfaces.ILinkAttrs),
    ]
    config = get_configurator('ewave', *utilities, settings=settings)
    config.register_menu(
        ('dataset', partial(menu_item, 'dataset', label='Home')),
        ('contributions', partial(menu_item, 'contributions')),
        ('parameters', partial(menu_item, 'parameters')),
        ('contributors', partial(menu_item, 'contributors')),
        ('sentences', partial(menu_item, 'sentences')),
    )

    config.register_map('contribution', LanguageMap)
    config.register_map('contributions', Map)

    config.register_adapter(
        GeoJsonContributions,
        interfaces.IContribution,
        interfaces.IIndex,
        name=GeoJsonContributions.mimetype)

    config.register_datatable('contributions', WaveContributions)
    config.register_datatable('parameters', Features)
    config.register_datatable('values', Values)
    return config.make_wsgi_app()
