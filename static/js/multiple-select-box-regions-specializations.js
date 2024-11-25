$(document).ready(function () {
    // Initialize Select2 on the 'regions' field
    $('#id_regions').select2({
        placeholder: 'Изберете области или градове:',
        multiple: true,  // Allow multiple selections
        closeOnSelect: false  // Keep dropdown open after selecting
    });
    $('#id_specializations').select2({
        placeholder: 'Изберете специалности:',
        multiple: true,
        closeOnSelect: false
    });

    $('#id_regions, #id_specializations').on('select2:open', function () {
        // Get the current width of the body
        var bodyWidth = $('body').outerWidth();

        // Apply 'overflow: hidden' to body and set the body width to prevent layout shift
        $('body').css({
            'overflow': 'hidden',
            'padding-right': window.innerWidth - bodyWidth + 'px'  // Account for scrollbar width
        });
    });

    // Re-enable scrolling when the Select2 dropdown closes
    $('#id_regions, #id_specializations').on('select2:close', function () {
        // Reset overflow and padding-right to restore layout
        $('body').css({
            'overflow': 'auto',
            'padding-right': '0'
        });
    });


});