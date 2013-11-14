<%inherit file="home_comp.mako"/>

<h3>Downloads</h3>

<div class="span5 well well-small">
    <dl>
    % for model, dls in h.get_downloads(request):
        <dt>${_(model)}</dt>
        % for dl in dls:
        <dd>
            <a href="${dl.url(request)}">${dl.label(req)}</a>
        </dd>
        % endfor
    % endfor
        <dt>The WAVE questionnaire</dt>
        <dd><a href="${request.static_url('ewave:static/WAVEquestionnaire.pdf')}">WAVEquestionnaire.pdf</a></dd>
    </dl>
</div>
<div class="span6">
    <p>
        <i>eWAVE</i> is published under a Creative Commons Attribution 3.0 License, so you are free
        to make use of and expand on our database for your own purposes, as long as you
        acknowledge <i>eWAVE</i> as your source. However, we would like to ask you, as a courtesy,
        to share the results of your work with us in turn. Please use our
        <a href="${request.route_url('contact')}">contact email address</a>
        to let us know about <i>eWAVE</i>-based work that you publish.
    </p>
    <p>
        Downloads are provided as
        ${h.external_link("http://en.wikipedia.org/wiki/Zip_%28file_format%29", label="zip archives")}
        bundling the data and a
        ${h.external_link("http://en.wikipedia.org/wiki/README", label="README")}
        file.
    </p>
</div>
