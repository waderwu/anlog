/* Formatting function for row details - modify as you need */
function format ( d ) {
    // `d` is the original data object for the row
    return '<table cellpadding="5" cellspacing="0" border="0" style="padding-left:500px;">'+
        '<tr>'+
            '<td>Headers:</td>'+
            '<td>'+d.fields.headers+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Post:</td>'+
            '<td>'+d.fields.post+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Get:</td>'+
            '<td>'+d.fields.get+'</td>'+
        '</tr>'+
        '<tr>'+
            '<td>Response:</td>'+
            '<td>'+d.fields.response+'</td>'+
        '</tr>'+
    '</table>';
}
 
$(document).ready(function() {
    var table = $('#example').DataTable( {
        dom: 'Bfrtip',
        buttons: [
            'selected',
            'selectedSingle',
            'selectAll',
            'selectNone',
            'selectRows',
        ],
        select: true,
        searching: false,
        ordering: false,
        "ajax": {
            "processing": true,
            "url": "{% url 'show' %}",
            "dataSrc": ""
        },
        "columns": [
            {
                "className":      'details-control',
                "orderable":      false,
                "data":           null,
                "defaultContent": ''
            },
            { "data": "name" },
            { "data": "position" },
            { "data": "office" },
            { "data": "salary" }
        ],
        "order": [[1, 'asc']]
    } );

     
    // Add event listener for opening and closing details
    $('#example tbody').on('click', 'td.details-control', function () {
        var tr = $(this).closest('tr');
        var row = table.row( tr );
 
        if ( row.child.isShown() ) {
            // This row is already open - close it
            row.child.hide();
            tr.removeClass('shown');
        }
        else {
            // Open this row
            row.child( format(row.data()) ).show();
            tr.addClass('shown');
        }
    } );
} );