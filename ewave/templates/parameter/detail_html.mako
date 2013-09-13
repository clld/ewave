<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "parameters" %>
<%block name="title">${_('Parameter')} ${ctx.name}</%block>

<h2>${_('Parameter')} ${ctx.name}</h2>

% if ctx.description:
<em>${ctx.description}</em>
<p>${ctx.jsondatadict.get('example_source')}</p>
% endif

% if request.map:
${request.map.render()}
% endif

<div class="tabbable">
    <ul class="nav nav-tabs">
        <li class="active"><a href="#tab1" data-toggle="tab">Values</a></li>
        <li><a href="#tab2" data-toggle="tab">Examples</a></li>
    </ul>
    <div class="tab-content" style="overflow: visible;">
        <div id="tab1" class="tab-pane active">
            <% dt = request.registry.getUtility(h.interfaces.IDataTable, 'values'); dt = dt(request, h.models.Value, parameter=ctx) %>
            ${dt.render()}
        </div>
        <div id="tab2" class="tab-pane">
            <%util:table items="${examples}" args="item">
                <%def name="head()">
                    <th>Example</th><th>Variety</th>
                </%def>
                <td>${h.link(request, item)}</td>
                <td>${h.link(request, item.language)}</td>
            </%util:table>
        </div>
    </div>
</div>
