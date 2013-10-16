<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

##<%def name="sidebar()">
##    <div class="well">
##    </div>
##</%def>

<h2>Welcome to eWAVE</h2>
<p>
    by ${request.dataset.formatted_editors()} ${h.cite_button(request, ctx)}
</p>

<p>
    WELCOME to the electronic World Atlas of Varieties of English! eWAVE was designed and compiled at the
    ${h.external_link('http://www.frias.uni-freiburg.de/', label='Freiburg Institute for Advanced Studies (FRIAS)')}
    and the English Department of the University of Freiburg, Germany, between 2008 and 2013. eWAVE is an interactive database on
    morphosyntactic variation in spontaneous spoken English mapping ${stats['features']} features from about a dozen
    ##<a href="http://www.ewave-atlas.org:80/welcome/introduction#grammar">
    domains of grammar
    ##</a>
    in ${stats['vl']} varieties of English
    (traditional dialects, high-contact mother-tongue Englishes, and indigenized second-language Englishes) and ${stats['vpc']} English-based
    Pidgins and Creoles in eight Anglophone world regions (Africa, Asia, Australia, British Isles, Caribbean, North America, Pacific,
    and the South Atlantic; see
    <a href="${request.route_url('languages')}">here</a> for a list). It was compiled from descriptive
    materials, naturalistic corpus data, and native speaker knowledge by a team of
    <a href="${request.route_url('contributors')}">${stats['informants']} contributors</a>, all leading experts in their fields, directed by
    <a href="${request.route_url('contact')}">Bernd Kortmann</a> and
    <a href="${request.route_url('contact')}">Kerstin Lunkenheimer</a>. eWAVE is unique not only in its coverage and
    user-friendliness, but also in being an open access resource. As such it has the potential for serving both as a teaching tool
    in academic teaching around the world and as an indispensable research tool by specialists in many different fields of linguistics,
    including creolistics, dialectology, dialect syntax, language change, language typology, sociolinguistics, second language acquisition,
    and the study of World Englishes and learner Englishes.
</p>
<p>
    eWAVE was partly designed and entirely programmed in collaboration with the
    ${h.external_link('http://www.eva.mpg.de/', label='Max Planck Institute for Evolutionary Anthropology')}
    (Leipzig),
    and is also hosted by the MPI. Since eWAVE is designed as an evolving interactive tool, we are planning to have annual
    ##<a href="http://www.ewave-atlas.org:80/welcome/introduction#future">
    updates
    ##</a>
    . A similar project is the MPI-EVA's
    ${h.external_link('http://apics-online.info', label='APiCS')}
    (Atlas of Pidgin and Creole Language Structures; edited by Michaelis, Maurer, Haspelmath and Huber), which appeared in 2013,
    both as a book atlas and as an electronic database like eWAVE.
</p>
<p>
    In January 2013 De Gruyter Mouton published in print the <i>Mouton World Atlas of Variation of English</i>,  which offers
    perspectivizing accounts of the data sets in eWAVE as well as large-scale comparisons and synopses across the
    individual variety types and Anglophone world regions. Read more
    ${h.external_link('http://www.degruyter.de/view/product/181631?rskey=FRLlvj&amp;result=1&amp;q=kortmann%20wave', label='here')}.
</p>

<h3>What eWAVE can do for you</h3>
<p>
    eWAVE facilitates the investigation of global-scale patterns of morphosyntactic variation in English and helps answering questions like the following:
    <ul>
	<li>Which features are most/least widespread across varieties of English worldwide?</li>
	<li>How many varieties of English worldwide share feature X?</li>
	<li>Is feature X restricted to or characteristic of a particular part of the English-speaking world?</li>
	<li>Is feature X restricted to or characteristic of a particular group of varieties?</li>
	<li>Does variety A have feature X?</li>
	<li>In which area of grammar does variety A differ most from variety B?</li>
    </ul>
    The information required to answer questions of this kind can be found in the central parts of eWAVE: the
    <a href="${request.route_url('languages')}">varieties index</a>, the <a href="${request.route_url('parameters')}">features index</a>,
    and the individual variety and feature profiles. These combine searchable catalogues of varieties and of morphosyntactic features with interactive maps,
    and allow you to explore in detail the distribution of features within and across varieties of English and English-based Pidgins and Creoles worldwide
    ##(see the <a href="http://www.ewave-atlas.org:80/help">help pages</a> for more details)
    . Ultimately, the information provided in eWAVE can also be used
    for the investigation of more general questions, such as the following: Which features generally are characteristic of a particular variety type
    (e.g. L2 varieties)? In which domain of grammar is there most/least heterogeneity/homogeneity among varieties of English worldwide? Are English-based
    pidgins and creoles as a group significantly different from other varieties in terms of morphosyntax?
</p>

<h3>How to cite eWAVE</h3>
<p>
    eWAVE in general can be referred to in the following way: ${h.cite_button(request, ctx)}
</p>
<blockquote>
    ${h.newline2br(citation.render(ctx, request))|n}
</blockquote>
##<p>
##    More information on how to cite individual parts of eWAVE can be found in the <a href="http://www.ewave-atlas.org/help">help pages</a>.
##</p>
