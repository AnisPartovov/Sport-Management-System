$(document).ready(function() {
    var apiUrl = $('#admin_competition_sport').data('api-url');
    
    // Initialize select2 for competition form
    $('#admin_competition_sport').select2({
        dropdownParent: $('#addCompetitionModal')
    });
    $('#admin_side_a, #admin_side_b').select2({
        dropdownParent: $('#addCompetitionModal')
    });

    function updateCompetitorOptions(excludeElement, includeElement, initial = false) {
        var excludeVal = excludeElement.val();
        var options = includeElement.find('option');
        options.each(function() {
            if ($(this).val() == excludeVal) {
                $(this).prop('disabled', true);
            } else {
                $(this).prop('disabled', false);
            }
        });
        includeElement.trigger('change');

        // If it's the initial update, set the value of includeElement to the first non-disabled option
        if (initial) {
            includeElement.val(includeElement.find('option:not([disabled]):first').val()).trigger('change');
        }
    }

    $('#admin_side_a').on('change', function() {
        updateCompetitorOptions($(this), $('#admin_side_b'));
    });

    $('#admin_side_b').on('change', function() {
        updateCompetitorOptions($(this), $('#admin_side_a'));
    });

    // Get API URL from the form field or use default
    if (!apiUrl) {
        apiUrl = '/api/competitors/';
    }

    $('#admin_competition_sport').on('change', function() {
        var sport_id = $(this).val();

        if (!sport_id) {
            $('#admin_side_a, #admin_side_b').html('<option value="">Select competitor</option>').trigger('change');
            return;
        }

        $.ajax({
            url: apiUrl,
            data: {
                'sport_id': sport_id
            },
            dataType: 'json',
            success: function(data) {
                var options = '<option value="">Select competitor</option>';
                for (var i = 0; i < data.length; i++) {
                    options += '<option value="' + data[i].id + '">' + data[i].name + '</option>';
                }
                $('#admin_side_a, #admin_side_b').html(options).trigger('change');
                updateCompetitorOptions($('#admin_side_a'), $('#admin_side_b'), true);
            },
            error: function(jqXHR, textStatus, errorThrown) {
                console.log('AJAX error:', textStatus, errorThrown);
            }
        });
    });

    // Reset form when modal is closed
    $('#addCompetitionModal').on('hidden.bs.modal', function () {
        $('#admin_competition_sport').val('').trigger('change');
        $('#admin_side_a, #admin_side_b').html('<option value="">Select competitor</option>').trigger('change');
    });
});

