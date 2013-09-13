<%inherit file="../home_comp.mako"/>
<%namespace name="util" file="../util.mako"/>

<%def name="sidebar()">
    <div class="well">
    </div>
</%def>

<h2>Welcome to ewave</h2>

<p class="lead">
</p>

<h3>Changes</h3>
<%util:table items="${request.dataset.jsondata['changes']['2013']}" args="item">
    <%def name="head()">
        <th>Variety</th><th>Parameter</th><th>Old Value</th><th>New Value</th>
    </%def>
    <td>${h.link(request, varieties[item[0]])}</td>
    <td>${h.link(request, features[item[1]])}</td>
    <td>${item[2]}</td>
    <td>${item[3]}</td>
</%util:table>
