from datetime import date
import re
from collections import defaultdict

from sqlalchemy.orm import joinedload
from clld.scripts.util import Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import bibtex
from clldutils.misc import slug
from pycldf import Sources

import ewave
from ewave import models

CODE_COLORS = {
    'A': 'fe3856',
    'B': 'ed9c07',
    'C': 'efe305',
    'D': 'f3ffb0',
    'X': 'e8e8e8',
    '?': 'ffffff',
}

VARIETY_TYPE_ICONS = {
    'L1t': {'shape': 's', 'color': 'f38847', 'broad': 'L1'},
    'L1c': {'shape': 'd', 'color': 'd22257', 'broad': 'L1'},
    'L2': {'shape': 'c', 'color': 'a0fb75', 'broad': 'L2'},
    'Cr': {'shape': 't', 'color': 'cb9a34', 'broad': 'P/C'},
    'P': {'shape': 'f', 'color': '4d6cee', 'broad': 'P/C'},
}


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=ewave.__name__,
        name='eWAVE',
        description='The Electronic World Atlas of Varieties of English',
        domain='ewave-atlas.org',
        published=date(2013, 11, 15),  # FIXME!
        license='http://creativecommons.org/licenses/by/3.0/',
        contact='bernd.kortmann@anglistik.uni-freiburg.de',
        jsondata={
            'license_icon': 'cc-by.png',
            'license_name': 'Creative Commons Attribution 3.0 Unported License'})
    DBSession.add(dataset)

    ed_pattern = re.compile('ed(?P<ord>[0-9]+)$')
    for c in args.cldf['contributors.csv']:
        contrib = data.add(
            common.Contributor,
            c['ID'],
            id=c['ID'],
            name=c['Name'],
            email=c['Email'],
            url=c['URL'],
            address=c['Address'],
        )
        m = ed_pattern.match(c['ID'])
        if m:
            common.Editor(dataset=dataset, contributor=contrib, ord=int(m.group('ord')))

    for fc in args.cldf['featurecategories.csv']:
        data.add(
            models.FeatureCategory, fc['ID'],
            id=fc['ID'], name=fc['Name'], description=fc['Description'])

    for vt in args.cldf['varietytypes.csv']:
        data.add(
            models.VarietyType, vt['ID'],
            id=vt['ID'],
            name=vt['Name'],
            description=vt['Description'],
            jsondata=VARIETY_TYPE_ICONS[vt['ID']],
        )

    for vt in args.cldf['regions.csv']:
        data.add(models.Region, vt['ID'], id=vt['ID'], name=vt['Name'])

    for lang in args.cldf['LanguageTable']:
        l = data.add(
            models.Variety, lang['ID'],
            id=lang['ID'],
            name=lang['Name'],
            latitude=lang['Latitude'],
            longitude=lang['Longitude'],
            abbr=lang['abbr'],
            region=data['Region'][lang['Region_ID']],
            type=data['VarietyType'][lang['Type_ID']],
        )
        c = data.add(
            models.WaveContribution, lang['ID'],
            id=str(lang['ID']),
            name=lang['Name'],
            description=lang['Description'],
            variety=l)
        for i, cid in enumerate(lang['Contributor_ID']):
            DBSession.add(common.ContributionContributor(
                contribution=c,
                contributor=data['Contributor'][cid],
                ord=i+1,
            ))

    for param in args.cldf['ParameterTable']:
        data.add(
            models.Feature, param['ID'],
            id=param['ID'],
            category=data['FeatureCategory'][param['Category_ID']],
            name=param['Name'],
            description=param['Description'],
            jsondata={'example_source': param['Example_Source']})


    for de in args.cldf['CodeTable']:
        data.add(
            common.DomainElement, de['ID'],
            id=de['ID'],
            parameter=data['Feature'][de['Parameter_ID']],
            name=de['Name'],
            description=de['Description'],
            jsondata={'color': CODE_COLORS[de['Name']]},
            number=de['Number'])

    for rec in bibtex.Database.from_file(args.cldf.bibpath):
        data.add(common.Source, slug(rec.id), _obj=bibtex2source(rec))

    for example in args.cldf['ExampleTable']:
        s = data.add(
            common.Sentence, example['ID'],
            id=example['ID'],
            name=example['Primary_Text'],
            gloss='\t'.join(example['Gloss']) if example['Gloss'] else None,
            comment=example['Comment'] or None,
            description=example['Translated_Text'] or None,
            language=data['Variety'][example['Language_ID']])

        for ref in example['Source']:
            sid, pages = Sources.parse(ref)
            DBSession.add(common.SentenceReference(
                sentence=s, source=data['Source'][sid], description=pages, key=sid))

    for value in args.cldf['ValueTable']:
        de = data['DomainElement'][value['Code_ID']]
        vs = data.add(
            common.ValueSet, value['ID'],
            id=value['ID'],
            contribution=data['WaveContribution'][value['Language_ID']],
            parameter=data['Feature'][value['Parameter_ID']],
            jsondata=de.jsondata,
            language=data['Variety'][value['Language_ID']])
        v = data.add(
            common.Value, value['ID'],
            id=value['ID'],
            domainelement=de,
            valueset=vs)

        for eid in value['Example_ID']:
            DBSession.add(common.ValueSentence(sentence=data['Sentence'][eid], value=v))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    nvarieties = DBSession.query(models.Variety.pk).count()

    for feature in DBSession.query(models.Feature).options(
        joinedload(common.Parameter.valuesets)
                .joinedload(common.ValueSet.values)
                .joinedload(common.Value.domainelement)
    ):
        values = defaultdict(lambda: 0)
        for vs in feature.valuesets:
            values[vs.values[0].domainelement.name] += 1
        attested = values['A'] + values['B'] + values['C']
        feature.attestation = attested / float(nvarieties)
        feature.pervasiveness = (values['A'] + 0.6 * values['B'] + 0.3 * values['C']) / attested
