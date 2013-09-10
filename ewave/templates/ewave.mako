<%inherit file="app.mako"/>

##
## define app-level blocks:
##
<%block name="header">
    <div id="header" class="container-fluid" style="border-bottom: 5px solid white; height: 80px; background-image: url(${request.static_url('ewave:static/banner2.png')})">
        <h1>
        ##    <a href="${request.route_url('dataset')}">${request.dataset.description}</a>
        </h1>
    </div>
</%block>

${next.body()}
