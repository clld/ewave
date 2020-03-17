<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">${ctx.name}</%block>

<h2>${ctx.name}</h2>
${h.coins(request, ctx)}
${h.text2html(ctx.description or '', mode='p', sep='\n')}

${request.get_datatable('values', h.models.Value, language=ctx.variety).render()}

<%def name="sidebar()">
    <%util:well title="Informant">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well>
        ${request.map.render()}
        ${h.format_coordinates(ctx.variety)}
    </%util:well>
</%def>
