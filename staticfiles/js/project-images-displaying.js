$(document).ready(function () {
    const $lightbox = $("<div class='lightbox'></div>");
    const $lightboxContent = $("<div class='lightbox-content'></div>");
    const $lightboxImg = $("<img class='lightbox-image'>");
    const $lightboxCaption = $("<div class='image-caption'></div>");
    const $prevButton = $("<button class='lightbox-arrow lightbox-arrow-left'>&lt;</button>");
    const $nextButton = $("<button class='lightbox-arrow lightbox-arrow-right'>&gt;</button>");

    $lightboxContent.append($prevButton, $lightboxImg, $lightboxCaption, $nextButton);
    $lightbox.append($lightboxContent);
    $("body").append($lightbox);

    let images = [];
    let captions = [];
    let currentIndex = 0;
    let currentProject = null;

    $lightbox.hide();

    // On image click inside the project
    $(".project-card-images img").click(function (e) {
        e.preventDefault();

        const $currentImage = $(this);
        currentProject = $currentImage.closest(".project-card"); // Store the current project

        // Collect image URLs and captions only for the current project
        images = currentProject.find(".project-card-images img").map(function () {
            return $(this).attr("src");
        }).get();

        captions = currentProject.find(".project-card-images .image-caption").map(function () {
            return $(this).text();
        }).get();

        currentIndex = images.indexOf($currentImage.attr("src")); // Find index of clicked image

        // Show image and caption
        showImage(currentIndex);

        $lightbox.fadeIn(); // Show the lightbox
    });

    // Show the image and caption based on the current index
    function showImage(index) {
        const $currentImage = currentProject.find(".project-card-images img").eq(index); // Find the image within the current project
        const captionText = $currentImage.siblings(".image-caption").text() || ''; // Get the caption

        $lightboxImg.attr("src", images[index]); // Set the image
        $lightboxCaption.text(captionText); // Set the caption

        if (captionText) {
            $lightboxCaption.show(); // Show caption if available
        } else {
            $lightboxCaption.hide(); // Hide caption if not available
        }
    }

    // Navigate to the previous image
    $prevButton.click(function () {
        currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
        showImage(currentIndex);
    });

    // Navigate to the next image
    $nextButton.click(function () {
        currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
        showImage(currentIndex);
    });

    // Handle keyboard navigation
    $(document).keydown(function (e) {
        if ($lightbox.is(":visible")) {
            if (e.key === "ArrowLeft") {
                currentIndex = (currentIndex > 0) ? currentIndex - 1 : images.length - 1;
                showImage(currentIndex);
            } else if (e.key === "ArrowRight") {
                currentIndex = (currentIndex < images.length - 1) ? currentIndex + 1 : 0;
                showImage(currentIndex);
            } else if (e.key === "Escape") {
                $lightbox.fadeOut();
            }
        }
    });

    // Close the lightbox when clicking outside of the content area
    $lightbox.click(function (e) {
        if ($(e.target).is($lightbox)) {
            $lightbox.fadeOut();
        }
    });
});
