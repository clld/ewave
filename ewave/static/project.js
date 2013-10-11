EWAVE = {};

EWAVE.toggle_languages = function(eid) {
    var i, j, feature, any,
        ctrl = $('#dt-filter-type'),
        checkboxes = {};
    $('input.vtype').each(function(i) {checkboxes[$(this).attr('value')] = $(this).prop('checked')});

    any = checkboxes['--any--'];

    CLLD.mapFilterMarkers(eid, function(marker){
        return any || checkboxes[marker.feature.properties.language.type.pk];
    });

    for (i in checkboxes) {
        if (checkboxes[i]) {
            if (i == '--any--') {
                i = '';
            }
            ctrl.val(i);
            CLLD.DataTables['Values'].fnFilter(i, $("tfoot .control").index(ctrl));
        }
    }
}
