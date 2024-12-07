document.addEventListener('DOMContentLoaded', function() {
    // Check if there are any validation errors in the form
    const form = document.querySelector('form');
    const errorMessages = form.querySelectorAll('.errorlist');  // Assuming error messages are rendered with the .errorlist class

    // If there are errors, scroll to the form section
    if (errorMessages.length > 0) {
        const formSection = document.querySelector('.form-section');
        if (formSection) {
            formSection.scrollIntoView({
                behavior: 'smooth',  // Smooth scrolling
                block: 'start'  // Scroll to the top of the form section
            });
        }
    }
});