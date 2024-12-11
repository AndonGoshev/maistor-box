document.addEventListener('click', function(event) {
    // Close the main dropdown menu if clicked outside
    const menuToggle = document.getElementById('menu-toggle');
    const menuWrapper = document.querySelector('.menu-wrapper');

    if (menuToggle.checked && !menuWrapper.contains(event.target)) {
        menuToggle.checked = false;
    }

    // Close the profile dropdown menu if clicked outside
    const profileMenuToggle = document.getElementById('profile-menu-toggle');
    const profileMenuWrapper = document.querySelector('.profile-menu-wrapper');

    if (profileMenuToggle.checked && !profileMenuWrapper.contains(event.target)) {
        profileMenuToggle.checked = false;
    }
});