<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>

<h2>${ctx.name}</h2>
${h.coins(request, ctx)}
${h.text2html(ctx.description or '', mode='p', sep='\n')}

${request.get_datatable('values', h.models.Value, language=ctx.variety).render()}

<%def name="sidebar()">
    <%util:well title="Author">
        ${h.linked_contributors(request, ctx)}
        ${h.cite_button(request, ctx)}
    </%util:well>
    <%util:well>
        ${request.map.render()}
    </%util:well>
    ##<%util:well title="Sources">
    ##<dl>
    ##    % for source in sorted(list(ctx.language.sources), key=lambda s: s.name):
    ##    <dt style="clear: right;">${h.link(request, source)}</dt>
    ##    <dd id="${h.format_gbs_identifier(source)}">${source.description}</dd>
    ##    % endfor
    ##</dl>
    ##${util.gbs_links(filter(None, [s.gbs_identifier for s in ctx.language.sources]))}
    ##</%util:well>
</%def>
