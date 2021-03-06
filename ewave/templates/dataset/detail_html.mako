<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>


<h2>eWAVE 3.0</h2>
<p>
    by ${request.dataset.formatted_editors()} ${h.cite_button(request, ctx)}
</p>
<p>
    Welcome to the new updated version of the electronic World Atlas of Varieties of English: eWAVE 3.0!
</p>

<h3>What is new?</h3>
<p>
    eWAVE 3.0 comprises an additional variety of English, i.e.
    <a href="${req.route_url('language', id='77')}">Croker Island English</a>, and thus counts 77 Englishes
    spoken around the world. It is the largest available database of English varieties up to date.
</p>
<p>
    eWAVE 3.0 includes new bibliographic references and examples. Some values for the various morphosyntactic features
    have been updated based on a survey among the 84 eWAVE contributors, directed by Bernd Kortmann and Katharina Ehret.
    Most notably, there have been substantial changes in the feature ratings of Kenyan English.
</p>
<p>
    The new version of eWAVE also contains Glottocodes for 65 of the 77 varieties based on the classification
    of Glottolog 4.2.1. These codes serve as unique and persistent identifiers and may facilitate
    computational matching and retrieval of specific varieties, also across different databases. However, in some
    cases, in particular for dialects of English, an exact one-to-one match between eWAVE varieties and the Glottolog
    classification was not possible.
</p>
<p>
    You can find a detailed description of all changes at
    ${h.external_link('https://github.com/cldf-datasets/ewave/compare/v2.0...v3.0', label='GitHub')}.
</p>


<h3>About</h3>
<p>
    eWAVE was designed and compiled at the
    ${h.external_link('http://www.frias.uni-freiburg.de/', label='Freiburg Institute for Advanced Studies (FRIAS)')}
    and the English Department of the University of Freiburg, Germany, primarily between 2008 and 2011,
    when it was first released. Release 2.0 (November 2013) was substantially updated and
    extended. eWAVE is an interactive database on
    morphosyntactic variation in spontaneous spoken English mapping ${stats['features']} features from a dozen
    domains of grammar in now ${stats['vl']} varieties of English
    (traditional dialects, high-contact mother-tongue Englishes, and indigenized second-language Englishes)
    and ${stats['vpc']} English-based
    Pidgins and Creoles in eight Anglophone world regions (Africa, Asia, Australia, British Isles, Caribbean, North
    America, Pacific,
    and the South Atlantic; see
    <a href="${request.route_url('languages')}">here</a> for a list). It was compiled from descriptive
    materials, naturalistic corpus data, and native speaker knowledge by a team of
    <a href="${request.route_url('contributors')}">${stats['informants']} contributors</a>, all leading experts in their
    fields, directed by
    <a href="${request.route_url('contact')}">Bernd Kortmann</a> and
    <a href="${request.route_url('contact')}">Kerstin Lunkenheimer</a>. eWAVE is unique not only in its coverage and
    user-friendliness, but also in being an open access resource. As such it has the potential for serving both as a
    teaching tool
    in academic teaching around the world and as an indispensable research tool for specialists in many different fields
    of linguistics,
    including creolistics, dialectology, dialect syntax, language change, language typology, sociolinguistics, second
    language acquisition,
    and the study of World Englishes and learner Englishes.
</p>
<p>
    eWAVE was partly designed and entirely programmed in collaboration with the
    ${h.external_link('http://www.eva.mpg.de/', label='Max Planck Institute for Evolutionary Anthropology')}
    (Leipzig),
    and is also hosted by the MPI. Since eWAVE is designed as an evolving interactive tool, we are planning to have
    regular updates.
    The most recent substantial update (November 2013) introduced two new datasets
    (<a href="${request.route_url('contribution', id='76')}">Cape Flats English</a> and
    <a href="${request.route_url('contribution', id='75')}">Philippine English</a>) as well
    as a number of updates to existing data points, a host of new examples, and substantial
    changes to the user interface to fit in with the architecture of the MPI-EVA’s other linguistic database
    projects – most notably ${h.external_link('http://apics-online.info', label='APiCS Online')}
    (the Atlas of Pidgin and Creole Language Structures Online; Michaelis, Maurer, Haspelmath and Huber, eds. 2013).
</p>
<p>
    In January 2013 De Gruyter Mouton published in print the <i>Mouton World Atlas of Variation of English</i>, which
    offers
    perspectivizing accounts of the data sets in eWAVE as well as large-scale comparisons and synopses across the
    individual variety types and Anglophone world regions. Read more
    ${h.external_link('http://www.degruyter.de/view/product/181631?rskey=FRLlvj&amp;result=1&amp;q=kortmann%20wave', label='here')}
    .
</p>

<h3>What eWAVE can do for you</h3>
<p>
    eWAVE facilitates the investigation of global-scale patterns of morphosyntactic variation in English and helps
    answering questions like the following:
</p>
<ul>
    <li>Which features are most/least widespread across varieties of English worldwide?</li>
    <li>How many varieties of English worldwide share feature X?</li>
    <li>Is feature X restricted to or characteristic of a particular part of the English-speaking world?</li>
    <li>Is feature X restricted to or characteristic of a particular group of varieties?</li>
    <li>Does variety A have feature X?</li>
    <li>In which area of grammar does variety A differ most from variety B?</li>
</ul>
<p>
    The information required to answer questions of this kind can be found in the central parts of eWAVE: the
    <a href="${request.route_url('languages')}">varieties index</a>, the <a href="${request.route_url('parameters')}">features
    index</a>,
    and the individual variety and feature profiles. These combine searchable catalogues of varieties and of
    morphosyntactic features with interactive maps,
    and allow you to explore in detail the distribution of features within and across varieties of English and
    English-based Pidgins and Creoles worldwide.
    Ultimately, the information provided in eWAVE can also be used
    for the investigation of more general questions, such as the following: Which features generally are characteristic
    of a particular variety type
    (e.g. L2 varieties)? In which domain of grammar is there most/least heterogeneity/homogeneity among varieties of
    English worldwide? Are English-based
    pidgins and creoles as a group significantly different from other varieties in terms of morphosyntax?
</p>

<h3>How to cite eWAVE</h3>
<p>
    eWAVE in general can be referred to in the following way: ${h.cite_button(request, ctx)}
</p>
<blockquote>
    ${h.newline2br(citation.render(ctx, request))|n}
</blockquote>
