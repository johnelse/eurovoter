$(document).ready(function() {
    $('input#submit').click(function() {
        $('div#results').html('Data submitted...');
        $.post('/formsubmit', $('form#voting').serialize(), function(data) {
                $('div#results').html(data)
            }
        );
    });
});
