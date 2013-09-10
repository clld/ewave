from __future__ import unicode_literals
import sys
from datetime import date
import os
import re
import csv
from collections import defaultdict
from functools import partial

from path import path
from clld.scripts.util import initializedb, Data
from clld.db.meta import DBSession
from clld.db.models import common

import ewave
from ewave import models


COL_PATTERN = re.compile('\s*`(?P<name>[^`]+)`\s*(?P<type>[a-z]+)')


def converter(type_, x):
    x = x.strip()
    if x == str(r'\N'):
        return None
    if type_ in ['int']:
        return int(x)
    return x.decode('utf8')


TYPE_MAP = defaultdict(lambda: partial(converter, 'text'), int=partial(converter, 'int'))


def read_schema(args, table):
    fields = []
    for line in file(args.data_file('%s.sql' % table)):
        if line.startswith('  `'):
            m = COL_PATTERN.match(line)
            if m.group('name').endswith('_id'):
                fields.append((m.group('name'), int))
            else:
                fields.append((m.group('name'), TYPE_MAP[m.group('type')]))
    return fields


def read(args, table):
    schema = read_schema(args, table)

    for row in csv.reader(file(args.data_file('%s.txt' % table)), delimiter=str('\t')):
        yield dict((schema[i][0], schema[i][1](v)) for i, v in enumerate(row))


def main(args):
    data = Data()

    dataset = common.Dataset(
        id=ewave.__name__,
        name='eWAVE',
        description='The Electronic World Atlas of Varieties of English',
        domain='ewave-atlas.org',
        published=date(2011, 8, 15),
        license='http://creativecommons.org/licenses/by-sa/3.0/',
        contact='bernd.kortmann@anglistik.uni-freiburg.de',
        jsondata={
            'license_icon': 'http://i.creativecommons.org/l/by-sa/3.0/88x31.png',
            'license_name': 'Creative Commons Attribution-ShareAlike 3.0 Unported License'})
    DBSession.add(dataset)

    #for id, name, description in [
    #    ('L1t', 'Low-contact traditional L1 dialects', 'Traditional, regional non-standard mother-tongue varieties, e.g. East Anglian English and the dialects spoken in the Southwest, the Southeast and the North of England, as well as, in North America, Newfoundland English, Appalachian English and Ozark English.'),
    #    ('L1c', 'High-contact L1 varieties', 'This includes transplanted L1 Englishes and colonial standards (e.g. Bahamian English, New Zealand English), as well as language shift varieties (e.g. Irish English) and standard varieties (e.g. colloquial American English, colloquial British English).'),
    #    ('L2', 'L2 varieties', 'Institutionalized indigenized non-native varieties like Pakistani English, Jamaican English, Hong Kong English, Ghanaian English and Kenyan English, but also non-native varieties that compete with local L1 varieties for institutional status, e.g. Chicano English and Black South African English.'),
    #    ('P', 'Pidgins', 'English-based contact languages that developed for communication between two groups who did not share the same language, typically in restricted domains of use (especially trade). With the exception of Butler English, all the English-based pidgins in eWAVE (e.g. Tok Pisin, Nigerian Pidgin and Ghanaian Pidgin) can be considered expanded pidgins, i.e. in contrast to prototypical pidgins they are less restricted in terms of domains of use, and many of them are spoken as native or primary languages by a considerable proportion of their speakers.'),
    #    ('C', 'Creoles', 'English-based contact languages that developed in settings where a non-English-speaking group was under strong pressure to acquire and use some form of English, while access to its L1 speakers was severely limited (e.g. in plantation settings). Many creoles have become the native language of the majority of the population. Examples of English-based creoles in the eWAVE set include Jamaican Creole, Belizean Creole, Sranan, and Torres Strait Creole.'),
    #]:

    icons = {
        'L1t': {'shape': 's', 'color': 'f38847'},
        'L1c': {'shape': 'd', 'color': 'd22257'},
        'L2': {'shape': 'c', 'color': 'a0fb75'},
        'Cr': {'shape': 't', 'color': 'cb9a34'},
        'P': {'shape': 'f', 'color': '4d6cee'},
    }

    for cat in read(args, 'language_cat'):
        cls = models.VarietyType if cat['name'] == 'cat1' else models.Region
        if cat['name'] == 'cat1' and cat['value'] not in icons:
            raise ValueError(cat['value'])
        data.add(
            cls, cat['value'],
            id=cat['value'],
            name=cat['name1'],
            description=cat['definition'],
            jsondata=icons.get(cat['value']))

    for lang in read(args, 'language'):
        keys = ['id', 'name', 'latitude', 'longitude']
        l = data.add(
            models.Variety, lang['id'],
            region=data['Region'][lang['cat2']],
            type=data['VarietyType'][lang['cat1']],
            **{k: v for k, v in lang.items() if k in keys})
        data.add(
            models.WaveContribution, lang['id'],
            id=str(lang['id']),
            name=lang['name'],
            description=lang['spec1'],
            variety=l)

    for author in read(args, 'o1_author'):
        c = data.add(
            common.Contributor, author['id'],
            id=str(author['id']), name="%(first_name)s %(last_name)s" % author)
        for lang in filter(None, [l.strip() for l in author['langIDs'].split(',')]):
            DBSession.add(common.ContributionContributor(
                contributor=c,
                contribution=data['WaveContribution'][int(lang)]))

    domain = {
        'A': ('feature is pervasive or obligatory', {'color': 'fe3856'}),
        'B': ('feature is neither pervasive nor extremely rare', {'color': 'ed9c07'}),
        'C': ('feature exists, but is extremely rare', {'color': 'efe305'}),
        'D': ('attested absence of feature', {'color': 'f3ffb0'}),
        'X': ('feature is not applicable (given the structural make-up of the variety/P/C)', {'color': 'e8e8e8'}),
        '?': ('no information on feature is available', {'color': 'ffffff'}),
    }

    for param in read(args, 'lparam'):
        data.add(
            common.Parameter, param['id'],
            id=str(param['id']),
            name=param['name'])

    for de in read(args, 'lparamshaping'):
        desc, jsondata = domain[de['name']]
        data.add(
            common.DomainElement, de['id'],
            id=str(de['id']),
            parameter=data['Parameter'][de['lparam_id']],
            name=de['name'],
            description=desc,
            jsondata=jsondata,
            number=de['number'])

    # values:
    for value in read(args, 'llps'):
        if not int(value['value']):
            continue
        de = data['DomainElement'][value['lparamshaping_id']]
        vs = data.add(
            common.ValueSet, value['id'],
            id=str(value['id']),
            contribution=data['WaveContribution'][value['language_id']],
            parameter=de.parameter,
            jsondata=de.jsondata,
            language=data['Variety'][value['language_id']])
        data.add(
            common.Value, value['id'],
            id=str(value['id']),
            domainelement=de,
            valueset=vs)

    for sentence in read(args, 'o2_sentence'):
        values = filter(None, [l.strip() for l in sentence['llpsdataIDs'].split(',')])
        assert values
        s = data.add(
            common.Sentence, sentence['id'],
            id=str(sentence['id']),
            name=sentence['primary_text'],
            language=data['Value'][int(values[0])].valueset.language,
            comment=sentence['spec2'])
        for value in values:
            DBSession.add(
                common.ValueSentence(sentence=s, value=data['Value'][int(value)]))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """


if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
