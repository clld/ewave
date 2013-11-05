<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">Datapoint ${ctx.language}/${ctx.parameter}</%block>


<h2>Datapoint ${ctx.language}/${ctx.parameter}</h2>

<table class="table table-nonfluid">
    <tbody>
        <tr>
            <th>Variety:</th>
            <td>${h.link(request, ctx.contribution)}</td>
        </tr>
        <tr>
            <th>Feature:</th>
            <td>${h.link(request, ctx.parameter)}</td>
        </tr>
        <tr>
            <th>Value:</th>
            <td>${ctx.values[0].domainelement.name} - ${ctx.values[0].domainelement.description}</td>
        </tr>
        <tr>
            <th>Informants:</th>
            <td>${h.linked_contributors(request, ctx.contribution)} ${h.cite_button(req, ctx.contribution)}</td>
        </tr>
    </tbody>
</table>

% if ctx.values[0].sentence_assocs:
<h3>Examples</h3>
${util.sentences(ctx.values[0])}
% endif
