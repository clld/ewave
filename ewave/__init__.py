from functools import partial

from clld.web.app import get_configurator, menu_item
from clld.web.icon import MapMarker
from clld import interfaces
from clld.web.adapters.download import Download
from clld.db.models import common

# we must make sure custom models are known at database initialization!
from ewave import models
from ewave.adapters import GeoJsonContributions


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
_('Changes')


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

        return super(WaveMapMarker, self).__call__(ctx, req)  # pragma: no cover


def link_attrs(req, obj, **kw):
    if interfaces.ILanguage.providedBy(obj):
        # we are about to link to a language details page: redirect to contribution page!
        kw['href'] = req.route_url('contribution', id=obj.id, **kw.pop('url_kw', {}))
    #if interfaces.IParameter.providedBy(obj):
    #    kw['label'] = '%s %s' % (obj.id, obj.name)
    if interfaces.IValueSet.providedBy(obj):
        kw['title'] = obj.values[0].domainelement.description
        kw['label'] = u'%s - %s' % (obj.values[0].domainelement.name, obj.values[0].domainelement.description)
    return kw


def main(global_config, **settings):
    """ This function returns a Pyramid WSGI application.
    """
    settings['route_patterns'] = {
        'contributors': '/authors',
        'contributor': '/authors/{id:[^/\.]+}',
        'contributions': '/languages',
        'contribution': '/languages/{id:[^/\.]+}',
        'languages': '/varieties',
        'language': '/varieties/{id:[^/\.]+}',
    }
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
        ('sources', partial(menu_item, 'sources')),
    )
    config.include('clldmpg')
    config.include('ewave.maps')
    config.include('ewave.datatables')
    config.include('ewave.adapters')
    return config.make_wsgi_app()
