# coding=utf8
from __future__ import unicode_literals
import sys
from datetime import date
import os
import sys
import re
import csv
from collections import defaultdict
from functools import partial

from sqlalchemy.orm import joinedload_all
import xlrd
from bs4 import BeautifulSoup as bs
from path import path
from clld.scripts.util import initializedb, Data, bibtex2source
from clld.db.meta import DBSession
from clld.db.models import common
from clld.lib import excel
from clld.lib import bibtex
from clld.util import slug

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


def examples(args, id_):
    def text(tag):
        return ' '.join(list(tag.stripped_strings)).strip()

    filename = args.data_file('%.2d.html' % id_)
    if filename.exists():
        with open(filename) as fp:
            soup = bs(fp.read())
        for tr in soup.find_all('tr'):
            tds = tr.find_all('td')
            try:
                fid = int(text(tds[0]))
            except:
                continue
            ps = tds[2].find_all('p')
            if id_ != 53 and len(ps) % 3 == 0:
                for i in range(0, len(ps), 3):
                    primary, gloss, translation = ps[i:i+3]
                    yield (fid, text(primary), text(gloss), text(translation))
            else:
                yield (fid, text(tds[2]), None, None)


def main(args):
    data = Data()

    def maybe_int(c):
        try:
            return int(c.value)
        except Exception:
            return None

    xls = xlrd.open_workbook(args.data_file('ewave.xls'))
    #var-infrmnts-type-regn-lat-lon
    #colour code matrix
    #RatingSystem&abbreviations
    #Feature Groups
    #Example sources
    varieties = {}
    values = {}
    matrix = xls.sheet_by_name('matrixRAW-quer')
    features = [maybe_int(matrix.cell(0, i)) for i in range(matrix.ncols)]

    for i in range(3, matrix.nrows):
        values[maybe_int(matrix.cell(i, 1))] = dict(
            (features[j], matrix.cell(i, j).value.upper()) for j in range(6, matrix.ncols) if features[j])

    features = {n: dict(name=matrix.cell(1, i).value) for i, n in enumerate(features)}

    sheet = xls.sheet_by_name('Example sources')
    for i in range(sheet.nrows):
        id = maybe_int(sheet.cell(i, 0))
        if id in features:
            features[id]['example'] = sheet.cell(i, 2).value
            features[id]['example_source'] = sheet.cell(i, 2).value

    sheet = xls.sheet_by_name('var-infrmnts-type-regn-lat-lon')
    for i in range(sheet.nrows):
        if i == 0:
            cols = [sheet.cell(i, j).value.lower() for j in range(sheet.ncols)]
        else:
            varieties[int(sheet.cell(i, 0).value)] = dict(
                (cols[j], sheet.cell(i, j).value) for j in range(sheet.ncols))

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
    common.Editor(dataset=dataset, contributor=common.Contributor(id='ed1', name='Bernd Kortmann'), ord=1)
    common.Editor(dataset=dataset, contributor=common.Contributor(id='ed2', name='Kerstin Lunkenheimer'), ord=2)

    for id, name, description in [
        ('1', 'Pronouns', 'Pronouns, pronoun exchange, nominal gender'),
        ('2', 'Noun Phrase', 'Noun phrase'),
        ('3', 'Tense & Aspect', 'Verb phrase I: tense and aspect'),
        ('4', 'Modal Verbs', 'Verb phrase II: modal verbs'),
        ('5', 'Verb Morphology', 'Verb phrase III: verb morphology'),
        ('6', 'Voice', 'Verb phrase IV: voice'),
        ('7', 'Negation', 'Negation'),
        ('8', 'Agreement', 'Agreement'),
        ('9', 'Relativization', 'Relativization'),
        ('10', 'Complementation', 'Complementation'),
        ('11', 'Adverbial Subordination', 'Adverbial Subordination'),
        ('12', 'Adverbs & Prepositions', 'Adverbs and prepositions'),
        ('13', 'Discourse & Word Order', 'Discourse organization and word order'),
    ]:
        data.add(
            models.FeatureCategory, name, id=id, name=name, description=description)

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
        data.add(
            common.Contributor, author['id'],
            id=str(author['id']), name="%(first_name)s %(last_name)s" % author)

    abbr2lang = {}
    new_langs = []
    for vid, v in varieties.items():
        if vid not in data['Variety']:
            new_langs.append(vid)
            l = data.add(
                models.Variety, vid,
                id=str(vid),
                name=v['variety'],
                latitude=v['latitude'],
                longitude=v['longitude'],
                region=[r for r in data['Region'].values() if r.name == v['world region']][0],
                type=data['VarietyType'][v['variety  type (narrow)']])
            contribution = data.add(
                models.WaveContribution, vid,
                id=str(vid),
                name=l.name,
                description='TODO',
                variety=l)
            if v['contributor(s)'] == 'Rajend Mesthrie':
                v['contributor(s)'] = 'Rajend Mesthrie and Tracey Toefy and Sean Bowerman'
            for name in v['contributor(s)'].split(' and '):
                contributor = None
                name = name.strip()
                maxid = 0
                for c in data['Contributor'].values():
                    if int(c.id) > maxid:
                        maxid = int(c.id)
                    if c.name == name:
                        contributor = c
                        print '--- already known:', name
                if not contributor:
                    maxid += 1
                    contributor = data.add(
                        common.Contributor, maxid, id=str(maxid), name=name)
                DBSession.add(common.ContributionContributor(
                    contributor=contributor, contribution=contribution))
        else:
            l = data['Variety'][vid]
        l.abbr = v['abbreviation'].strip()
        abbr2lang[l.abbr] = l

    for author in read(args, 'o1_author'):
        for lang in filter(None, [l.strip() for l in author['langIDs'].split(',')]):
            DBSession.add(common.ContributionContributor(
                contributor=data['Contributor'][author['id']],
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
            models.Feature, param['id'],
            id=str(param['id']),
            category=data['FeatureCategory'][param['cat1']],
            name=param['name'],
            description=param['name1'],
            jsondata={'example_source': param['spec1']})

    for de in read(args, 'lparamshaping'):
        desc, jsondata = domain[de['name']]
        data.add(
            common.DomainElement, de['id'],
            id=str(de['id']),
            parameter=data['Feature'][de['lparam_id']],
            name=de['name'],
            description=desc,
            jsondata=jsondata,
            number=de['number'])

    # values:
    changes = []
    maxid = 0
    for value in read(args, 'llps'):
        if not int(value['value']):
            continue
        if value['id'] > maxid:
            maxid = value['id']
        de = data['DomainElement'][value['lparamshaping_id']]
        if de.name != values[value['language_id']][int(de.parameter.id)]:
            new_de = None
            for _de in de.parameter.domain:
                if _de.name == values[value['language_id']][int(de.parameter.id)]:
                    new_de = _de
                    break
            if not new_de or new_de == de:
                print values[value['language_id']][int(de.parameter.id)], ' =?= ', de.name
            changes.append((str(value['language_id']), de.parameter.id, de.name, values[value['language_id']][int(de.parameter.id)]))
            de = new_de
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

    dataset.jsondata['changes'] = {'2013': changes}
    print len(changes), 'values changed'

    for new_lang in new_langs:
        for param, value in values[new_lang].items():
            if new_lang == 75 and param == 195 and not value:
                value = '?'
            maxid += 1
            parameter = data['Feature'][param]
            de = None
            for _de in parameter.domain:
                if _de.name == value:
                    de = _de
            assert de
            vs = data.add(
                common.ValueSet, maxid,
                id=str(maxid),
                contribution=data['WaveContribution'][new_lang],
                parameter=parameter,
                jsondata=de.jsondata,
                language=data['Variety'][new_lang])
            data.add(
                common.Value, maxid,
                id=str(maxid),
                domainelement=de,
                valueset=vs)

    DBSession.flush()

    for rec in bibtex.Database.from_file(args.data_file('eWAVE2References_tidy-1.bib')):
        data.add(common.Source, slug(rec.id), _obj=bibtex2source(rec))

    for i, example in enumerate(excel.rows(xlrd.open_workbook(args.data_file('eWAVE2-Examples_tidy-1.xlsx')).sheets()[0], as_dict=True)):
        lang = abbr2lang[example['language']]
        if isinstance(example['feature number'], basestring):
            fid = re.match('([0-9]+)', example['feature number']).groups()[0]
        else:
            fid = example['feature number']
        fid = str(int(fid))
        s = data.add(
            common.Sentence, i+1,
            id=str(i+1),
            name=example['primary_text'],
            gloss=example['gloss'] or None,
            comment=example['comment'] or None,
            description=example['translation'] or None,
            language=lang)

        for ref in (example['Source'] or '').split(';'):
            if ref:
                ref = ref.strip()
                desc = None
                if ':' in ref:
                    ref, desc = [_s.strip() for _s in ref.split(':', 1)]
                recid = slug(ref)
                recid = {
                    'allsopp996': 'allsopp1996',
                    'orton1962': 'orton19621971',
                    'bbcvoices': 'voices',
                    'cottmann1963': 'cottman1963',
                    'mooreetal1991': 'moore1991',
                }.get(recid, recid)
                if recid not in data['Source']:
                    assert recid == '50'
                DBSession.add(common.SentenceReference(
                    sentence=s, source=data['Source'][recid], description=desc, key=ref))

        vs = DBSession.query(common.ValueSet)\
            .join(common.Parameter).join(common.Language)\
            .filter(common.Parameter.id == fid)\
            .filter(common.Language.pk == lang.pk).one()
        DBSession.add(common.ValueSentence(sentence=s, value=vs.values[0]))


def prime_cache(args):
    """If data needs to be denormalized for lookup, do that here.
    This procedure should be separate from the db initialization, because
    it will have to be run periodiucally whenever data has been updated.
    """
    nvarieties = DBSession.query(models.Variety.pk).count()

    for feature in DBSession.query(models.Feature).options(joinedload_all(
        common.Parameter.valuesets, common.ValueSet.values, common.Value.domainelement
    )):
        values = defaultdict(lambda: 0)
        for vs in feature.valuesets:
            values[vs.values[0].domainelement.name] += 1
        attested = values['A'] + values['B'] + values['C']
        feature.attestation = attested / float(nvarieties)
        feature.pervasiveness = (values['A'] + 0.6 * values['B'] + 0.3 * values['C']) / attested

if __name__ == '__main__':
    initializedb(create=main, prime_cache=prime_cache)
    sys.exit(0)
