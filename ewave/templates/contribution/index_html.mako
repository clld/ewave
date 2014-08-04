<%inherit file="../${context.get('request').registry.settings.get('clld.app_template', 'app.mako')}"/>
<%namespace name="util" file="../util.mako"/>
<%! active_menu_item = "contributions" %>
<%block name="title">Varieties</%block>


<h2>Varieties</h2>

${request.get_map('contributions', col={c.name: c for c in ctx.cols}.get('type')).render()}

<div>
    ${ctx.render()}
</div>
