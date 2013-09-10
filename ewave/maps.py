from clld.web.maps import LanguageMap as BaseLanguageMap


class LanguageMap(BaseLanguageMap):
    """small map on contribution detail page
    """
    def __init__(self, ctx, req, eid='map'):
        super(LanguageMap, self).__init__(ctx.variety, req, eid=eid)
