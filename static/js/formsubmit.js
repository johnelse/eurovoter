var SCORES = [12, 10, 8, 7, 6, 5, 4, 3, 2, 1]

function has_duplicates(sorted_list) {
    for (i = 0; i < (sorted_list.length - 1); i++) {
        if (sorted_list[i] == sorted_list[i + 1]) {
            return true;
        };
    };

    return false;
}

$(document).ready(function() {
    $('input#submit').click(function() {
        var submitted_country_ids = [];
        SCORES.forEach(function(score) {
            var country_id = $('select#' + score + 'points').val();
            if (country_id != 'None') {
                submitted_country_ids.push(country_id)
            };
        });

        submitted_country_ids.sort();
        if (has_duplicates(submitted_country_ids)) {
            $('div#results').html('Duplicates detected');
        }
        else {
            $('div#results').html('Data submitted...');
            $.post('/formsubmit', $('form#voting').serialize(), function(data) {
                    $('div#results').html(data)
                }
            );
        };
    });
});
