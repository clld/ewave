<%inherit file="home_comp.mako"/>
<%namespace name="clldmpgutil" file="clldmpg_util.mako"/>

<h3>Downloads</h3>

<p>
    <i>eWAVE</i> is published under a Creative Commons Attribution 3.0 License, so you are free
    to make use of and expand on our database for your own purposes, as long as you
    acknowledge <i>eWAVE</i> as your source. However, we would like to ask you, as a courtesy,
    to share the results of your work with us in turn. Please use our
    <a href="${request.route_url('contact')}">contact email address</a>
    to let us know about <i>eWAVE</i>-based work that you publish.
</p>
<p>
    <a href="${req.resource_url(req.dataset)}">eWAVE</a>
    serves the latest
    ${h.external_link('https://github.com/cldf-datasets/ewave/releases', label='released version')}
    of data curated at
    ${h.external_link('https://github.com/cldf-datasets/ewave', label='cldf-datasets/ewave')}.
    All released versions are accessible via <br/>
    <a href="https://doi.org/10.5281/zenodo.3603136">
        <img src="https://zenodo.org/badge/DOI/10.5281/zenodo.3603136.svg" alt="DOI">
    </a>
    <br/>
    on
    ${h.external_link('https://zenodo.org', label='Zenodo')}
    as well.
</p>

<p>
    You may also download the
    <a href="${request.static_url('ewave:static/WAVEquestionnaire.pdf')}">WAVE questionnaire [PDF]</a>.
</p>
