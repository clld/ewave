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

"""
refs = {
    (
        'Aceto, Michael',
        '2008',
        "Eastern Caribbean English-derived language varieties: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 645-660"),
    (
        'Alo, M.A. and Rajend Mesthrie',
        '2008',
        "Nigerian Pidgin English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 323-339"),
    #(
    #    'APiCS questionnaire. "Questionnaire" and feature pages on the website of the Atlas of Pidgin and Creole Language Structures, ed. by Susanne Michaelis, Philippe Maurer, Magnus Huber, Martin Haspelmath. http://lingweb.eva.mpg.de/apics/index.php/APiCS_Questionnaire.  Viewed 14th January 2009."),
    (
        'Baskaran, Loga',
        '2008',
        "Malaysian English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 610-623"),
    (
        'Beal, Joan',
        '2008',
        "English dialects in the North of England: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp. 373-403"),
    (
        'Bhatt, Rakesh M',
        '2008',
        "Indian English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 546-562"),
    (
        'Bowerman, Sean', '2008',
        "White South African English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 472-487"),
    (
        'Burridge, Kate',
        '2008',
        "Synopsis: morphological and syntactic variation in the Pacific and Australasia.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp. 583-600"),
    (
        'Clarke, Sandra',
        '2008',
        "Newfoundland English: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 492-509"),
    (
        'Crowley, Terry',
        '2008',
        "Bislama: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp.444-466"),
    (
        'Escure, Geneviève',
        '2008',
        "Belize and other central American varieties: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 732-762"),
    (
        'Faraclas, Nicholas',
        '2008',
        "Nigerian Pidgin English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 340-367"),
    (
        'Filppula, Markku',
        '2008',
        "Irish English: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp. 328-359"),
    (
        'Hickey, Raymond',
        '2004',
        "Appendix 1: Checklist of nonstandard features",
        "In: Raymond Hickey, ed. Legacies of Colonial English. Studies in transported dialects. Cambridge: CUP, pp. 586-620"),
    (
        'Huber, Magnus and Kari Dako',
        '2008',
        "Ghanaian English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 368-380"),
    (
        'Huber, Magnus',
        '2008',
        "Ghanaian Pidgin English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 381-394"),
    (
        'Huttar, Mary L',
        '2007',
        "Ndyuka (Creole English)",
        "In: Peter L. Patrick and John Holm, eds. Comparative creole syntax. Parallel Outlines of 18 Creole Grammars. UK/Sri Lanka: Battlebridge, pp. 217-236"),
    (
        'James, Winford and Valerie Youssef',
        '2008',
        "The creoles of Trinidad and Tobago: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 661-692"),
    (
        'Jourdan, Christine',
        '2008',
        "Solomon Islands Pijin: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp. 467-487"),
    (
        'Kautzsch, Alexander',
        '2008',
        "Earlier African American Vernacular English: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 534-550"),
    (
        'Kortmann, Bernd and Benedikt Szmrecsanyi',
        '2004',
        "Global synopsis: morphological and syntactic variation in English",
        "In: Bernd Kortmann, Edgar W. Schneider, Kate Burridge, Rajend Mesthrie, and Clive Upton, eds. A Handbook of Varieties of English. Vol. 2 Morphology and Syntax. Berlin/New York: Mouton de Gruyter."),
    (
        'Kortmann, Bernd',
        '2005',
        "English linguistics: essentials. Berlin: Cornelsen"),
    (
        'Kortmann, Bernd',
        '2008',
        "Synopsis: morphological and syntactic variation in the British Isles.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp.478-495"),
    (
        'Malcolm, Ian G',
        '2008',
        "Australian Creoles and Aboriginal English: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp. 415-443"),
    (
        'McCormick, Kay',
        '2008',
        "Cape Flats English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 521-534"),
    (
        'Melchers, Gunnel',
        '2008',
        "English spoken in Orkney and Shetland: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp.285-298"),
    (
        'Mesthrie, Rajend and Rakesh M. Bhatt',
        '2008',
        "World Englishes: The study of new linguistic varieties. Cambridge: Cambridge University Press"),
    (
        'Mesthrie, Rajend',
        '2008a',
        "Black South African English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 488-500"),
    (
        'Mesthrie, Rajend',
        '2008b',
        "Indian South African English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 501-520"),
    (
        'Mesthrie, Rajend',
        '2008c',
        "Synopsis: morphological and syntactic variation in Africa and South and Southeast Asia.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 624-635"),
    (
        'Miller, Jim',
        '2008',
        "Scottish English: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp.299- 327"),
    (
        'Montgomery, Michael B',
        '2008',
        "Appalachian English: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 428-467"),
    (
        'Mufwene, Salikoko S',
        '2008',
        "Gullah: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 551-571"),
    (
        'Mugler, France and Jan Tent',
        '2008',
        "Fiji English: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp. 546-567"),
    (
        'Mühlhäusler, Peter',
        '2008',
        "Norfolk Island-Pitcairn English (Norfuk and Pitkern): morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp.568-582"),
    (
        'Murray, Thomas E. and Beth Lee Simon',
        '2008',
        "Colloquial American English: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 401-427"),
    (
        'Patrick, Peter L',
        '2007',
        "Jamaican Patwa (Creole English)",
        "In: Peter L. Patrick and John Holm, eds. Comparative creole syntax. Parallel Outlines of 18 Creole Grammars. UK/Sri Lanka: Battlebridge, pp. 127-152"),
    (
        'Patrick, Peter L',
        '2008',
        "Jamaican Creole: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 607-644"),
    (
        'Peter, Lothar and Hans-Georg Wolf',
        '2007',
        "A comparison of the varieties of West African Pidgin English",
        "In: World Englishes 26(1):3-21"),
    (
        'Sakoda, Kent and Jeff Siegel',
        '2008',
        "Hawai'i Creole: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp. 514-545"),
    (
        'Schmied, Josef',
        '2008',
        "East African English (Kenya, Uganda, Tanzania): morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 451-471"),
    (
        'Schneider, Edgar W',
        '2007',
        "Postcolonial English. Varieties around the world. Cambridge: Cambridge University Press"),
    (
        'Schneider, Edgar W',
        '2008',
        "Synopsis: morphological and syntactic variation in the Americas and the Caribbean.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 763-776"),
    (
        'Sharma, Devyani',
        '2005',
        "Language transfer and discourse universals in Indian English article use.",
        "Studies in Second Language Acquisition 27: 535-566"),
    (
        'Singler, John V',
        '2008',
        "Liberian Settler English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 395-415"),
    (
        'Smith, Geoff',
        '2008',
        "Tok Pisin: morphology and syntax.",
        "In: Kate Burridge and Bernd Kortmann, eds. Varieties of English. Vol. 3: The Pacific and Australasia. Berlin/New York: Mouton de Gruyter, pp.488-513"),
    (
        'Trudgill, Peter and J. J. Chambers, eds',
        '1991',
        'Dialects of English: studies in grammatical variation. London: Longman.'),
    (
        'Trudgill, Peter',
        '2008',
        "The dialect of East Anglia: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol.1: The British Isles. Berlin/New York: Mouton de Gruyter, pp. 404-416"),
    (
        'Upton, Clive, David Parry and J. D. A. Widdowson',
        '1994',
        "Survey of English dialects: the dictionary and grammar. London: Routledge."
    (
        'Wagner, Susanne',
        '2008',
        "Dialects in the Southwest of England: morphology and syntax.",
        "In: Bernd Kortmann and Clive Upton, eds. Varieties of English. Vol. 1: The British Isles. Berlin/New York: Mouton de Gruyter, pp.417-439"),
    (
        'Wee, Lionel.',
        "Singapore English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 593-609"),
    (
        'Wilson, Sheila and Rajend Mesthrie',
        '2008',
        "St. Helena English: morphology and syntax.",
        "In: Rajend Mesthrie, ed. Varieties of English. Vol. 4: Africa, South and Southeast Asia. Berlin/New York: Mouton de Gruyter, pp. 535-545"),
    (
        'Winford, Donald and Bettina Migge',
        "Surinamese creoles: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 693-731"),
    (
        'Wolfram, Walt',
        '2008a',
        "Rural and ethnic varieties in the Southeast: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 468-491"),
    (
        'Wolfram, Walt',
        '2008b',
        "Urban African American Vernacular English: morphology and syntax.",
        "In: Edgar W. Schneider, ed. Varieties of English. Vol.2: The Americas and the Caribbean. Berlin/New York: Mouton de Gruyter, pp. 510-533"),
    (
        'Yillah, Sorie M and Chris Corcoran',
        '2007',
        "Krio (Creole English)",
        "In: Peter L. Patrick and John Holm, eds. Comparative Creole Syntax. Parallel Outlines of 18 Creole Grammars. UK/Sri Lanka: Battlebridge, pp. 175-198"),
}
"""


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

    ex = {}
    maxid = 0
    for sentence in read(args, 'o2_sentence'):
        if sentence['id'] > maxid:
            maxid = sentence['id']
        values = filter(None, [l.strip() for l in sentence['llpsdataIDs'].split(',')])
        assert values
        s = data.add(
            common.Sentence, sentence['id'],
            id=str(sentence['id']),
            name=sentence['primary_text'],
            language=data['Value'][int(values[0])].valueset.language,
            comment=sentence['spec2'])
        for value in values:
            value = data['Value'][int(value)]
            DBSession.add(common.ValueSentence(sentence=s, value=value))
            ex[(int(value.valueset.language.id), int(value.valueset.parameter.id))] = 1

    for lid in range(100):
        for fid, example, gloss, translation in examples(args, lid):
            if (lid, fid) in ex:
                continue
            maxid += 1
            s = data.add(
                common.Sentence, maxid,
                id=str(maxid),
                name=example,
                analyzed=example if gloss else None,
                gloss=gloss,
                description=translation,
                language=data['Variety'][lid])
            vs = DBSession.query(common.ValueSet)\
                .join(common.Parameter).join(common.Language)\
                .filter(common.Parameter.id == str(fid))\
                .filter(common.Language.id == str(lid)).one()
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
