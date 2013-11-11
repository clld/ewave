<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${ctx.id} ${ctx.name}</%block>

<ul class="nav nav-pills pull-right">
    <li><a href="#map-container">Map</a></li>
    <li><a href="#list-container">List</a></li>
</ul>

<h2>${ctx.id} ${ctx.name}</h2>

<div class="row-fluid">
    <div class="span7">
        <%util:well>
            ${u.value_table(ctx, request)}
        </%util:well>
    </div>
    % if ctx.description:
    <div class="span5">
        <dl>
            <dt>Feature area:</dt>
            <dd>${ctx.category.description}</dd>
            <dt>Typical example:</dt>
            <dd><i>${ctx.description}</i></dd>
            <dt>Example source:</dt>
            <dd>${ctx.jsondatadict.get('example_source')}</dd>
        </dl>
    </div>
    % endif
</div>

${request.map.render()}

${util.values_and_sentences()}
