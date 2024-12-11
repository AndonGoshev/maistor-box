$(document).ready(function () {
    // Function to initialize Select2 on given selectors with specific options
    function initializeSelect2(selector, options) {
        $(selector).select2(options);

        // Handle Select2 open event for scroll disabling
        $(selector).on('select2:open', function () {
            var bodyWidth = $('body').outerWidth();
            $('body').css({
                'overflow': 'hidden',
                'padding-right': window.innerWidth - bodyWidth + 'px'
            });
        });

        // Handle Select2 close event for restoring scroll
        $(selector).on('select2:close', function () {
            $('body').css({
                'overflow': 'auto',
                'padding-right': '0'
            });
        });
    }

    // Read the select mode from the script's data attribute
    var selectMode = $('script[src*="select-box-regions-specializations.js"]').data('select-mode');

    // Determine options based on the select mode
    var isMultiple = selectMode === 'multiple';

    // Set placeholders dynamically
    var regionPlaceholder = isMultiple ? 'Къде работите?' : 'Изберете област или град:';
    var specializationPlaceholder = isMultiple ? 'Изберете специалности:' : 'Изберете специалност:';

    // Initialize Select2 with dynamic placeholders
    initializeSelect2('#id_regions', {
        placeholder: regionPlaceholder,
        multiple: isMultiple,
        closeOnSelect: !isMultiple
    });

    initializeSelect2('#id_specializations', {
        placeholder: specializationPlaceholder,
        multiple: isMultiple,
        closeOnSelect: !isMultiple
    });
});