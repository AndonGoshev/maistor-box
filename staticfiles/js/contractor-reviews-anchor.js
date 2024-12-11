document.addEventListener('DOMContentLoaded', function() {
    // Check if there are any validation errors in the form
    const form = document.querySelector('form');
    const errorMessages = form.querySelectorAll('.errorlist'); // Assuming error messages are rendered with the .errorlist class

    // If there are errors, scroll to the form section anchor
    if (errorMessages.length > 0) {
        const formSection = document.querySelector('#form-section-anchor'); // Use the correct ID
        if (formSection) {
            formSection.scrollIntoView({
                behavior: 'smooth',  // Smooth scrolling
                block: 'start'  // Scroll to the top of the form section
            });

            // Clear the hash in the URL to prevent interference
            if (window.location.hash) {
                history.replaceState(null, null, ' '); // Removes the hash without reloading
            }
        }
    }

    // Handle anchor link click for the feedback section
    const anchorLink = document.querySelector('a[href="#feedbacks-section-anchor"]');
    if (anchorLink) {
        anchorLink.addEventListener('click', function(event) {
            event.preventDefault(); // Prevent default anchor behavior (jumping)
            const feedbackSection = document.querySelector('#feedbacks-section-anchor');

            if (feedbackSection) {
                feedbackSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }

            // Update the hash in the URL manually
            history.replaceState(null, null, '#feedbacks-section-anchor');
        });
    }
});