<%inherit file="home_comp.mako"/>
<%namespace name="util" file="util.mako"/>

<%block name="head">
<style type="text/css">
/*<![CDATA[*/
        @page {  }
        table { border-collapse:collapse; border-spacing:0; empty-cells:show }
        td, th { vertical-align:top;}
        <!-- "li span.odfLiEnd" - IE 7 issue-->
        * { margin:0;}
        .P16 { text-align:center ! important; }
        .P17 { margin-left:0.5in; margin-right:0in; text-indent:0in; }
        .P18 { margin-top:0.0835in; margin-bottom:0in; }
        .P19 { margin-left:0.55in; margin-right:0in; text-indent:-0.55in; }
        .P2 { font-weight:bold; }
        .P20 { margin-left:0.55in; margin-right:0in; text-indent:-0.55in; }
        .P21 { margin-left:0.55in; margin-right:0in; text-indent:-0.55in; }
        .P22 { font-weight:bold; margin-bottom:0.0417in; margin-top:0.1665in; }
        .P23 { font-style:normal; font-weight:bold; margin-bottom:0.0417in; margin-top:0.1665in; }
        .P24 { font-weight:bold; }
        .P25 { margin-bottom:0.0827in; margin-top:0.1945in; }
        .P26 { margin-bottom:0.0827in; margin-top:0in; }
        .P27 { margin-bottom:0.0827in; margin-top:0in; }
        .P28 { margin-bottom:0.0827in; margin-top:0in; text-align:center ! important; }
        .P29 { margin-bottom:0.0827in; margin-top:0in; text-align:center ! important; font-weight:bold; }
        .P3 { font-weight:bold; }
        .P30 { margin-bottom:0.0827in; margin-top:0in; font-weight:bold; }
        .P31 { margin-bottom:0.0827in; margin-top:0in; text-align:center ! important; font-style:italic; font-weight:bold; }
        .P32 { margin-bottom:0.0827in; margin-top:0in; }
        .P33 { margin-bottom:0.0827in; margin-top:0in; }
        .P34 { margin-bottom:0.0827in; margin-top:0in; }
        .P35 { margin-bottom:0in; margin-top:0in; }
        .P36 { margin-bottom:0in; margin-top:0in; }
        .P4 { text-align:center ! important; font-weight:bold; }
        .P5 { font-weight:bold; }
        .P8 { text-align:center ! important; }
        .P9 { font-weight:bold; }
        .Table1 { width:6.4076in; margin-left:-0.0736in; }
        .Table2 { width:6.0653in; margin-left:-0.0625in; }
        .Table3 { width:10.0181in; margin-left:-0.075in; }
        .Table1_A1 { vertical-align:top; padding:0.0417in; border-left-width:0.0399cm; border-left-style:double; border-left-color:#000000; border-right-style:none; border-top-width:0.0399cm; border-top-style:double; border-top-color:#000000; border-bottom-width:0.0399cm; border-bottom-style:double; border-bottom-color:#000000; }
        .Table1_B1 { vertical-align:middle; padding:0.0417in; border-left-width:0.0399cm; border-left-style:double; border-left-color:#000000; border-right-style:none; border-top-width:0.0399cm; border-top-style:double; border-top-color:#000000; border-bottom-width:0.0399cm; border-bottom-style:double; border-bottom-color:#000000; }
        .Table1_E1 { vertical-align:middle; padding:0.0417in; border-width:0.0399cm; border-style:double; border-color:#000000; }
        .Table1_E3 { vertical-align:top; padding:0.0417in; border-width:0.0399cm; border-style:double; border-color:#000000; }
        .Table2_A1 { vertical-align:middle; padding-left:0.0486in; padding-right:0.0486in; padding-top:0in; padding-bottom:0in; border-left-width:0.0399cm; border-left-style:double; border-left-color:#000000; border-right-style:none; border-top-width:0.0399cm; border-top-style:double; border-top-color:#000000; border-bottom-width:0.0399cm; border-bottom-style:double; border-bottom-color:#000000; }
        .Table2_D1 { vertical-align:middle; padding-left:0.0486in; padding-right:0.0486in; padding-top:0in; padding-bottom:0in; border-width:0.0399cm; border-style:double; border-color:#000000; }
        .Table3_A1 { vertical-align:top; padding-left:0.075in; padding-right:0.075in; padding-top:0in; padding-bottom:0in; border-style:none; }
        .Table1_A { width:1.0097in; }
        .Table1_B { width:1.3167in; }
        .Table1_C { width:1.4049in; }
        .Table1_E { width:1.3597in; }
        .Table2_A { width:2.5965in; }
        .Table2_B { width:1.0479in; }
        .Table2_D { width:1.3729in; }
        .Table3_A { width:10.0181in; }
/*]]>*/
</style>
</%block>

<%def name="sidebar()">
    <%util:well title="Contents">
    <ul class="nav nav-pills nav-stacked">
        <li><a href="#history">History and people behind <i>eWAVE</i></a></li>
        <li><a href="#varieties">The 76 varieties, Pidgins and Creoles in the <i>WAVE</i> sample</a></li>
        <li><a href="#types">Variety types covered</a></li>
        <li><a href="#domains">Domains of grammar covered in <i>WAVE</i></a></li>
        <li><a href="#ratings">Feature ratings</a></li>
        <li><a href="#statistics"><i>eWAVE 2.0</i> statistics</a></li>
        <li><a href="#limitations">Limitations and research potential of feature ratings</a></li>
        <li><a href="#future">The future of <i>eWAVE</i></a></li>
        <li><a href="#acknowledgements">Acknowledgements</a></li>
        <li><a href="#references">References</a></li>
    </ul>
    </%util:well>
</%def>


<h3>Introduction</h3>
<p>
    by ${request.dataset.formatted_editors()} ${h.cite_button(request, request.dataset)}
</p>

<%util:section id="history" level="${4}">
    <%def name="title()">
        History and people behind <i>eWAVE</i>
    </%def>
    <p>As a follow-up of the interactive CD-ROM accompanying the Mouton de Gruyter
    <i>Handbook of Varieties of English</i> (Kortmann, Schneider et al., eds. 2004),
    it was in 2008 that Bernd Kortmann and Kerstin Lunkenheimer joined forces in designing
    a considerably larger and more fine-grained database that could be
    used as an even more informative, less L1-centred research tool in
    comparative cross-dialectal and cross-varietal studies trying to
    map grammatical variation in the Anglophone world. In close
    collaboration with leading experts on the different variety types
    (including Lieselotte Anderwald, Susanne Michaelis, Rajend
    Mesthrie, Peter Mühlhäusler, Jeff Siegel, Peter Trudgill and
    Susanne Wagner) successive versions of a questionnaire were
    designed and discussed, before the version underlying
    <i>eWAVE</i>, with its 235
    morphosyntactic features, was decided upon and sent out to the
    informants. One reason for (a) considerably extending the scope of
    morphosyntactic variation to be documented and (b) choosing the
    programming format was that right from the start
    <i>eWAVE</i> was meant to allow
    immediate comparisons with other large databases on grammatical
    variation, notably <i>WALS</i>
    (${h.external_link('http://wals.info', label="The World Atlas of Language Structures")};
    Dryer and Haspelmath, eds. 2011) and
    <i>APiCS Online</i>
    (${h.external_link('http://apics-online.info', label="Atlas of Pidgin and Creole Structures Online")};
    Michaelis, Maurer, Haspelmath, Huber, eds. 2013), both developed at
    the
    ${h.external_link('http://www.eva.mpg.de/', label="Max Planck Institute for Evolutionary Anthropology (Leipzig)")}.
    It was a unique opportunity that the same people who were trusted with
    programming <i>APiCS</i> were also allowed to spend a significant amount of their time
    programming <i>eWAVE</i>.</p>
</%util:section>

<%util:section id="varieties" level="${4}">
    <%def name="title()">
        The 76 varieties, Pidgins and Creoles in the <i>eWAVE</i> sample
    </%def>
    <p>Table 1 provides an overview of the varieties,
    Pidgins and Creoles sampled in <i>eWAVE</i> and
    their distribution across variety types (see below) and world
    regions.</p>
    <p class="P24">Table <a id="refTable0" name="refTable0"></a>1:
    <i>eWAVE</i> varieties</p>
<table border="0" cellspacing="0" cellpadding="0" class="Table1">
<colgroup>
<col width="112" />
<col width="146" />
<col width="156" />
<col width="146" />
<col width="151" /></colgroup>
<tr class="Table11">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td colspan="2" style="text-align:left;width:1.3167in;" class=
"Table1_B1">
<p class="P29">L1 (32)</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_B1">
<p class="P29">L2 (18)</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E1">
<p class="P29">P (7) &amp; C (19)</p>
</td>
</tr>
<tr class="Table12">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_B1">
<p class="P31">low-contact L1 (10)</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_B1">
<p class="P31">high-contact L1 (21)</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_B1">
<p class="P28">&nbsp;</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E1">
<p class="P28">&nbsp;</p>
</td>
</tr>
<tr class="Table13">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">British Isles (11):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">Orkney and Shetland E, North of England, SW of
England, SE of England, East Anglia, Scottish E</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P32">Irish E, Welsh E, Manx E, Channel Islands E<br />
[Maltese E]</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P32">&nbsp;</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P27">British Creole</p>
</td>
</tr>
<tr class="Table14">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">Africa (17):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P27">Liberian Settler E,<br />
White South African E, White Zimbabwean E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">Ghanaian E, Nigerian E, Cameroon E, Kenyan E,
Tanzanian E, Ugandan E, Black South African E, Indian South African
E, Cape Flats E</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P27">Ghanaian Pidgin, Nigerian Pidgin, Cameroon Pidgin,
Krio, Vernacular Liberian E</p>
</td>
</tr>
<tr class="Table15">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">South Atlantic (3)</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P26">St. Helena E, Tristan da Cunha E, Falkland Islands
E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P26">&nbsp;</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P26">&nbsp;</p>
</td>
</tr>
<tr class="Table14">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">America (10):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P35">Newfoundland E, Appalachian E, Ozark E,</p>
<p class="P25">Southeast American Enclave dialects</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P27">Colloquial American E, Urban African American
Vernacular E, Rural African American Vernacular E, Earlier African
American Vernacular E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">Chicano E</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P27">Gullah</p>
</td>
</tr>
<tr class="Table17">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">Caribbean (13):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P27">Bahamian E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">Jamaican E</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P36">Jamaican C, Bahamian C, Barbadian C (Bajan)</p>
<p class="P25">Belizean C, Trinidadian C, Eastern Maroon C, Sranan,
Saramaccan, Guyanese C, San Andrés C, Vincentian C</p>
</td>
</tr>
<tr class="Table15">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">South and Southeast Asia (8):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P27">Colloquial Singapore E, Philippine E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P32">Indian E, Pakistan E, Sri Lanka E, Hong Kong E,
Malaysian E</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P27">Butler E</p>
</td>
</tr>
<tr class="Table19">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">Australia (5):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P32">Aboriginal E, Australian E, Australian Vernacular
E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P32">&nbsp;</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P33">Torres Strait C, Roper River C (Kriol)</p>
</td>
</tr>
<tr class="Table110">
<td style="text-align:left;width:1.0097in;" class="Table1_A1">
<p class="P30">Pacific (8):</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P27">&nbsp;</p>
</td>
<td style="text-align:left;width:1.4049in;" class="Table1_A1">
<p class="P27">New Zealand E</p>
</td>
<td style="text-align:left;width:1.3167in;" class="Table1_A1">
<p class="P32">Colloquial Fiji E, Acrolectal Fiji E,</p>
</td>
<td style="text-align:left;width:1.3597in;" class="Table1_E3">
<p class="P34">Hawaiian C, Bislama, Norf’k, Palmerston E,<br />
Tok Pisin</p>
</td>
</tr>
</table>
</%util:section>


<%util:section title="Variety types covered" id="types" level="${4}">
<p>The 76 data sets in the <i>eWAVE</i> sample fall into 5
broad classes of variety types, listed and briefly characterized
below. The experts were asked to classify “their” variety as
belonging to one of these variety types.</p>

<%util:section title="Traditional L1 varieties (L1t)" id="L1t" level="${5}">
<p>The varieties in this group are traditional,
regional non-standard varieties which are long-established
mother-tongue varieties and are characterized by a relatively low
degree of contact with other dialects or other languages since the
beginning of the colonial period (i.e. within approximately the
last 400 years).</p>
</%util:section>

<%util:section title="High-contact L1 varieties (L1c)" id="L1c" level="${5}">
<p class="P12">As the label suggests, the varieties in this group
are characterized by a high degree of contact between different
dialects of English and/or between English and other languages. The
following three types of varieties are considered high-contact L1
varieties in <i>eWAVE</i>:</p>
<ol type="lower-alpha">
<li>
Transplanted L1
Englishes or colonial standards, i.e. relatively new indigenized
varieties that arose roughly within the last 400 years, had native
speakers from early on and were formed by settlers with diverse
linguistic and/or dialectal backgrounds. They typically emerged in
territories that are former settlement colonies, and some, e.g. New
Zealand English or Australian English, have developed an
independent standard that is increasingly being recognized both
within the community and elsewhere. Others, such as Bahamian
English, or Channel Islands English, are closer in status to
traditional regional dialects.
</li>
<li>
Language-shift
Englishes, i.e. varieties that have replaced the erstwhile primary
language in the community and that have adult and child L1 and L2
speakers forming one speech community. Some of these varieties,
e.g. Irish English and Welsh English, also have shifted entirely,
and do no longer have significant numbers of L2 speakers.
</li>
<li>
Standard L1 varieties
</li>
</ol>
</%util:section>

<%util:section title="Indigenized L2 varieties (L2)" id="L2" level="${5}">
<p class="P12">We use this label to refer to two types of
non-native varieties. The first and larger group are non-native
indigenized varieties that emerged in territories where English was
introduced in the colonial era, typically via the education system,
and is still used in education and other official domains, but
where L1 speakers of metropolitan varieties were never present in
significant numbers. These varieties usually do not have
significant numbers of native speakers, but many enjoy some degree
of prestige and normative status in their political communities. An
example in <i>eWAVE</i> is Pakistani English.</p>
<p class="P12">The second group of L2 varieties are non-native
varieties spoken in territories where L1 speakers of English are
(or used to be) present in significant numbers, or even form the
majority of the population, but contact between L1 and L2 speakers
nevertheless is (or used to be) limited. These varieties are
‘indigenized’ to the extent that they are recognizable as distinct
varieties, but they typically do not have prestige or normative
status. Examples of this type in the <i>eWAVE</i> set are Chicano English
in the US and the English of the Black and Indian ethnic
communities in South Africa.</p>
</%util:section>

<%util:section title="English-based Pidgins (P)" id="P" level="${5}">
<p class="P12">English-based contact varieties (or rather, contact
languages) that typically developed in trade colonies for the
purpose of communication between two or more groups of speakers
that did not share a common language. Full acquisition of the
English language has in most cases not been the target. Initially,
pidgins are nobody’s mother tongue and are usually restricted to
certain domains of use (often as lingua francas). However, they may
over time acquire native speakers and also enter further domains of
use (extended/expanded pidgins). With the exception of Butler
English, all the English-based pidgins in eWAVE can be considered
expanded pidgins.</p>
</%util:section>

<%util:section title="English-based Creoles (Cr)" id="Cr" level="${5}">
<p class="P12">English-based contact varieties (or rather: contact
languages) that typically developed in settings (often in
plantation colonies) where a group of non-English speakers acquired
some variety of English. Typically, there was strong pressure upon
the non-English speaking group to use the language of the
socio-economically superior group (i.e. English), while exposure to
its native speakers was normally very limited. In the Caribbean,
for example, the proportion of native (and L2) speakers of English
was rather low in contrast to non-English speakers (who constantly
arrived in the colonies in large numbers). Many creoles have become
the native language of the majority of the population.</p>
</%util:section>
</%util:section>


<%util:section id="domains" level="${4}">
    <%def name="title()">
        Domains of grammar covered in  <i>eWAVE</i>
    </%def>
<p class="P11">The 235 features in <i>eWAVE</i>
cover phenomena from 12 different grammatical domains. An overview
is provided in Table 2 below.</p>
<p class="P9">&nbsp;</p>
<p class="P24"><span class="T7">Table</span> <a id="refTable1"
name="refTable1"></a>2<span class="T7">: Domains of grammar covered
in</span> <i>eWAVE</i></p>
<table border="0" cellspacing="0" cellpadding="0" class="Table2">
<colgroup>
<col width="288" />
<col width="116" />
<col width="116" />
<col width="152" /></colgroup>
<tr class="Table21">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P2">Grammatical domain</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P4">Features (number)</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P4">Sum features in group</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P4">% of total features</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Pronouns</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">1-47</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">47</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">20.0%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Noun phrase</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">48-87</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">40</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">17.0%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Tense and aspect</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">88-120</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">33</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">14.0%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Modal verbs</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">121-127</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">7</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">3.0%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Verb morphology</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">128-153</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">26</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">11.1%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Negation</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">154-169</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">16</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">6.8%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Agreement</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">170-184</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">15</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">6.4%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Relativization</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">185-199</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">15</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">6.4%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Complementation</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">200-210</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">11</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">4.7%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Adverbial subordination</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">211-215</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">5</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">2.1%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P7">Adverbs and prepositions</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">216-222</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">7</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P8">3.0%</p>
</td>
</tr>
<tr class="Table22">
<td style="text-align:left;width:2.5965in;" class="Table2_A1">
<p class="P10">Discourse organziation and word order</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">223-235</p>
</td>
<td style="text-align:left;width:1.0479in;" class="Table2_A1">
<p class="P8">13</p>
</td>
<td style="text-align:left;width:1.3729in;" class="Table2_D1">
<p class="P16">5.5%</p>
</td>
</tr>
</table>
</%util:section>


<%util:section id="ratings" level="${4}">
    <%def name="title()">
        Feature ratings
    </%def>
<p>The information in the <i>eWAVE</i>
database consists of judgements by top experts on each of the 76
varieties, Pidgins and Creoles on the frequency with which each of
the 235 features can be encountered in the relevant variety,
Pidgin, or Creole. The following classifications were used:</p>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <td>A</td><td>feature is pervasive or obligatory</td>
        </tr>
        <tr>
            <td>B</td><td>feature is neither pervasive nor extremely rare</td>
        </tr>
        <tr>
            <td>C</td><td>feature exists, but is extremely rare</td>
        </tr>
        <tr>
            <td>D</td><td>attested absence of feature</td>
        </tr>
        <tr>
            <td>X</td><td>feature is not applicable (given the structural make-up of the variety/P/C)</td>
        </tr>
        <tr>
            <td>?</td><td>no information on feature is available</td>
        </tr>
    </tbody>
</table>
</%util:section>

<%util:section id="statistics" level="${4}">
    <%def name="title()">
        <i>eWAVE 2.0</i> statistics
    </%def>
    <ol>
        <li>
            <strong>Attestation</strong>
            <p>
                Attestation is a relative measure of how widespread a feature is in the set of eWAVE varieties.
                It is expressed as a percentage and is calculated as the sum of all A-, B- and C-ratings for a
                feature, divided by the number of varieties in the eWAVE dataset. The closer the value to 100%,
                the more widespread the feature is.
            </p>
        </li>
        <li>
            <strong>Pervasiveness</strong>
            <p>
                Pervasiveness provides a measure of how pervasive a feature is on average in the varieties in
                which it is attested. Pervasiveness is calculated as all A-ratings for a feature plus 0.6 times
                the B-ratings for the same feature plus 0.3 times the C-ratings, divided by the sum of all
                A-, B- and C-ratings for the feature. This value is then multiplied by 100 and expressed as a
                percentage. A Pervasiveness value of 100% or close to 100% thus indicates that the feature is
                highly pervasive (rated A) in all or most of the varieties for which it is attested, while a
                value close to 30% (the lowest possible value) indicates that the feature is extremely rare
                (rated C) in most or all of the varieties for which it is attested. Intermediate values are less
                easy to interpret – here one has to look more closely at the ratio of A- to B- to C-values. Two
                more things should also be noted here:
            </p>
            <ol>
                <li>The Pervasiveness value does not provide information on how widespread a feature is in the
                    entire eWAVE dataset, i.e. for how many varieties the feature is actually attested.</li>
                <li>Since the eWAVE contributors did not all use exactly the same strategies in deciding when
                    to give a feature an A- vs. a B- or a C- vs. a B- rating, it is very difficult to translate
                    the ratings into numerical values that adequately reflect the differences between A-, B-
                    and C-ratings. The choice made here (1 for A, 0.6 for B and 0.3 for C) is certainly only
                    one of many, and further testing is required to see how adequate this model is.</li>
            </ol>
    </ol>
</%util:section>

<%util:section title="Limitations and research potential of feature ratings" id="limitations" level="${4}">
    <p>It should be obvious that in large-scale surveys
    such as <i>eWAVE</i>, <i>APiCS</i> or <i>WALS</i>, feature
    ratings need to be taken with a grain of salt. What looks
    categorical can hardly be more than an abstraction of and
    approximation to linguistic and social reality. Each of the
    varieties, Pidgins and Creoles included in <i>eWAVE</i> is itself subject to internal variation so that
    the profile emerging from the <i>WAVE</i>
    questionnaire for a given variety is unlikely to perfectly match
    the linguistic behaviour of any particular subgroup of speakers of
    that variety (e.g. different age groups). This is particularly true
    for the English-based Pidgins and Creoles and for the L2 varieties
    in the database. Typically, they have ethnically and socially
    diverse speech communities, so that features attested in
    <i>WAVE</i> may not be present in some speakers,
    or may be present with a different frequency, depending on which
    other languages they speak, and whether they are mesolectal,
    acrolectal or basilectal speakers. <i>WAVE</i>
    also glosses over regional variation in large speech communities
    like India or North America, when it subsumes them under one
    variety (‘Indian English’ and ‘Colloquial American English’).
    Moreover, the frequency-based ratings in most cases reflect the
    individual expert’s judgements since for many of the varieties,
    Pidgins and Creoles corpus data are not available at all, or only
    to a limited extent.
    </p>
    <p>There is an enormous research potential behind each
    of these caveats, pointing to the fact that <i>eWAVE</i> is at least as much a starting-point for new
    research as it is the outcome of prior research. For example, for
    anyone working within variationist sociolinguistics or within the
    emerging field of variationist pragmatics (especially the
    pragmatics of grammar) it will be fascinating to zoom in on the
    individual data points of the <i>eWAVE</i> feature
    set. Especially promising in this respect are all the features
    rated 'B' or 'C' since they are the prime candidates for glossing
    over 'orderly heterogeneity'.</p>
</%util:section>


<%util:section id="future" level="${4}">
    <%def name="title()">
        The future of  <i>eWAVE</i>
    </%def>
    <p>The database <i>eWAVE</i> is
    '<i>e</i>' in a double sense: it is electronic and
    it is e-volving. It is designed as something dynamic, as a
    constantly growing and improving teaching and research tool.
    &nbsp;Thus, since the launch of <i>eWAVE</i>
    <i>1.0</i> in November 2011, quite a few changes
    and improvements have been made. With regard to the data, the most
    important of these are a number of corrections to feature ratings,
    the addition of two completely new data
    sets (Philippine English and Cape Flats English), and more than
    2,400 new examples. Other new features include a list of
    references, export of filtered tables, and changes in filtering
    tools, navigation and general layout to fit in with the general
    architecture of <i>APiCS</i> and <i>WALS</i>.
    </p>
    <p>We plan to continue updating and expanding
    <i>eWAVE</i> in the future, and as before we
    welcome the comments and suggestions of the international research
    community and all users. This will help <i>eWAVE</i> to continually gain in reliability, strength and
    richness as a tool in academic teaching and research.</p>
</%util:section>


<%util:section title="Acknowledgements" id="acknowledgements" level="${4}">
    <p>There are many people and institutions, to some
    extent also lucky coincidences, <i>eWAVE</i> would
    have been impossible without. To start with, the two editors
    gratefully acknowledge the support of the
    ${h.external_link('http://www.frias.uni-freiburg.de', label="Freiburg Institute for Advanced Studies (FRIAS)")}
    in the design and data collection phase of the project. Bernd
    Kortmann enjoyed an Internal Senior Fellowship at the FRIAS from
    April 2008 until September 2009 and Kerstin Lunkenheimer joined him
    there as a research assistant from September 2008 until March 2009.
    Kerstin and Bernd are also most indebted to the Max Planck
    Institute for Evolutionary Anthropology (Leipzig), particularly to
    Susanne Michaelis and Martin Haspelmath for much helpful advice,
    for letting us piggyback on their projects, for offering to host
    <i>eWAVE</i> on the MPI server and, above all, for
    giving permission to their brilliant in-house linguist programmers
    Hagen Jung, Hans-Jörg Bibiko and Robert Forkel to work on
    <i>eWAVE</i> alongside APiCS. Hagen did a
    fantastic job in the early stages, calmly listened to all the ideas
    on what this new research tool was meant to do and never tired in
    providing improved versions of <i>eWAVE</i> and
    searching for optimal solutions, often surprising the editors with
    new ideas, fascinating visualizations and query options that they
    had never thought possible. Hans-Jörg and Robert made sure that
    everything continued to work as both <i>eWAVE</i>
    and <i>APiCS</i> evolved, and made the transition
    from <i>eWAVE 1.0</i> to <i>eWAVE 2.0</i> as smooth as we could only wish.
    </p>
    <p>Above all, the editors would like to thank the 83
    collaborators serving as informants for this project. Without their
    readiness to devote a significant amount of their precious time to
    filling in the questionnaire, providing examples and answering our
    questions, <i>eWAVE</i> would have been
    impossible. A crucial motivation for making <i>eWAVE</i> available as an open access resource thus was
    that <i>eWAVE</i> should be owned by the entire
    research community, as a dynamic resource and platform that
    continues to be improved and expanded and that will serve as a
    point of reference as much as a point of departure in teaching and
    research on varieties of English all around the world.</p>
</%util:section>


<%util:section title="References" id="references" level="${4}">
<table border="0" cellspacing="0" cellpadding="0" class="Table3">
<colgroup>
<col width="1112" /></colgroup>
<tr class="Table31">
<td style="text-align:left;width:10.0181in;" class="Table3_A1">
<p class="P19"><span class="T7">Kortmann, Bernd, Edgar W.
Schneider, Kate Burridge, Rajend Mesthrie and Clive Upton, eds.
2004.</span> <i>The Handbook of Varieties of
English. A multimedia reference tool.</i> Two
volumes plus CD-ROM. Berlin/New York: Mouton de Gruyter.</p>
</td>
</tr>
<tr class="Table31">
<td style="text-align:left;width:10.0181in;" class="Table3_A1">
<p class="P20">Dryer, Matthew S. and Martin Haspelmath,eds. 2011.
<i>The World Atlas of Language Structures
Online</i>. Munich: Max Planck Digital Library. Available online
at &lt;http://wals.info/&gt;, accessed 2011-07-28.</p>
</td>
</tr>
<tr class="Table31">
<td style="text-align:left;width:10.0181in;" class="Table3_A1">
<p class="P21">Michaelis, Susanne Maria, Philippe Maurer, Martin Haspelmath and Magnus Huber, eds. 2013.
<i>Atlas of Pidgin and Creole Language Structures Online</i>.
Leipzig: Max Planck Institute for Evolutionary Anthropology.
(Available online at http://apics-online.info, Accessed on 2013-11-04.)
</p>
</td>
</tr>
</table>
</%util:section>
