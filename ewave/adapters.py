from clld.web.adapters.geojson import GeoJsonLanguages


class GeoJsonContributions(GeoJsonLanguages):
    def get_language(self, ctx, req, item):
        return item.variety
