import pytest


@pytest.mark.parametrize(
    "method,path",
    [
        ('get_html', '/'),
        ('get_html', '/languages'),
        ('get_dt', '/languages'),
        ('get_dt', '/languages?iSortingCols=1&iSortCol_0=3&sSearch_3=a'),
        ('get_dt', '/languages?iSortingCols=1&iSortCol_0=4&sSearch_4=a'),
        ('get_html', '/languages/1'),
        ('get_json', '/languages.geojson'),
        ('get_dt', '/sentences?iSortingCols=1&iSortCol_0=3&sSearch_3=a'),
        ('get_html', '/parameters'),
        ('get_dt', '/parameters?iSortingCols=1&iSortCol_0=4&sSearch_4=a'),
        ('get_html', '/parameters/1'),
        ('get_json', '/parameters/1.geojson'),
        ('get_dt', '/values'),
        ('get_dt', '/values?language=1'),
        ('get_dt', '/values?parameter=1&iSortingCols=1&iSortCol_0=2&sSearch_2=a'),
        ('get_dt', '/values?parameter=1&iSortingCols=1&iSortCol_0=3&sSearch_3=a'),
        ('get_html', '/sources'),
        ('get_html', '/sources/apics'),
    ])
def test_pages(app, method, path):
    getattr(app, method)(path)
