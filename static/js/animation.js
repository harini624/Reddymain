
/* =====================================================
   HOMEPAGE MOBILE CAROUSELS
   Categories, Featured Properties, Why Choose Us
   ===================================================== */

document.addEventListener("DOMContentLoaded", function () {
    const mobileQuery = window.matchMedia("(max-width: 600px)");
    const reducedMotionQuery = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    const selectors = [
        ".categories .category-grid",
        ".featured .property-grid",
        ".why-us .why-grid"
    ];

    selectors.forEach(function (selector) {
        const track = document.querySelector(selector);

        if (!track) return;

        // Do not create a carousel for a single card.
        const cards = Array.from(track.children).filter(function (card) {
            return card.matches(
                ".category, .property-card, .empty-state, .why-card"
            );
        });

        if (cards.length < 2) return;

        // Create a viewport without changing the card contents.
        let viewport = track.parentElement;

        if (!viewport.classList.contains("re-home-carousel-viewport")) {
            viewport = document.createElement("div");
            viewport.className = "re-home-carousel-viewport";

            track.parentNode.insertBefore(viewport, track);
            viewport.appendChild(track);
        }

        // Create navigation dots.
        const dots = document.createElement("div");
        dots.className = "re-home-carousel-dots";
        dots.setAttribute("aria-label", "Carousel navigation");

        viewport.insertAdjacentElement("afterend", dots);

        let currentIndex = 0;
        let timer = null;
        let touchStartX = 0;
        let touchStartY = 0;

        const buttons = cards.map(function (_, index) {
            const button = document.createElement("button");

            button.type = "button";
            button.setAttribute("aria-label", "Show slide " + (index + 1));

            button.addEventListener("click", function () {
                currentIndex = index;
                updateSlide();
                restartTimer();
            });

            dots.appendChild(button);
            return button;
        });

        function updateSlide() {
            if (!mobileQuery.matches) {
                track.style.transform = "";
                return;
            }

            const slideWidth = viewport.clientWidth;

            track.style.transform =
                "translate3d(-" + (currentIndex * slideWidth) + "px, 0, 0)";

            buttons.forEach(function (button, index) {
                const active = index === currentIndex;

                button.classList.toggle("is-active", active);
                button.setAttribute("aria-current", active ? "true" : "false");
            });
        }

        function showNextSlide() {
            currentIndex = (currentIndex + 1) % cards.length;
            updateSlide();
        }

        function stopTimer() {
            if (timer !== null) {
                window.clearInterval(timer);
                timer = null;
            }
        }

        function startTimer() {
            stopTimer();

            if (
                !mobileQuery.matches ||
                reducedMotionQuery.matches ||
                document.hidden
            ) {
                return;
            }

            timer = window.setInterval(showNextSlide, 4000);
        }

        function restartTimer() {
            startTimer();
        }

        function handleTouchStart(event) {
            if (!mobileQuery.matches || !event.changedTouches.length) return;

            touchStartX = event.changedTouches[0].clientX;
            touchStartY = event.changedTouches[0].clientY;

            stopTimer();
        }

        function handleTouchEnd(event) {
            if (!mobileQuery.matches || !event.changedTouches.length) {
                startTimer();
                return;
            }

            const touch = event.changedTouches[0];
            const deltaX = touch.clientX - touchStartX;
            const deltaY = touch.clientY - touchStartY;

            // Only treat a clear horizontal gesture as a slide.
            if (Math.abs(deltaX) > 40 && Math.abs(deltaX) > Math.abs(deltaY)) {
                if (deltaX < 0) {
                    currentIndex = (currentIndex + 1) % cards.length;
                } else {
                    currentIndex =
                        (currentIndex - 1 + cards.length) % cards.length;
                }

                updateSlide();
            }

            startTimer();
        }

        function enableCarousel() {
            const isMobile = mobileQuery.matches;

            track.classList.toggle("re-home-carousel-active", isMobile);
            dots.classList.toggle("is-visible", isMobile);

            if (!isMobile) {
                currentIndex = 0;
                track.style.transform = "";
                return;
            }

            updateSlide();
        }

        viewport.addEventListener("touchstart", handleTouchStart, {
            passive: true
        });

        viewport.addEventListener("touchend", handleTouchEnd, {
            passive: true
        });

        viewport.addEventListener("mouseenter", stopTimer);
        viewport.addEventListener("mouseleave", startTimer);

        viewport.addEventListener("focusin", stopTimer);
        viewport.addEventListener("focusout", startTimer);

        window.addEventListener("resize", updateSlide);

        mobileQuery.addEventListener("change", function () {
            stopTimer();
            enableCarousel();
            startTimer();
        });

        reducedMotionQuery.addEventListener("change", startTimer);

        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                stopTimer();
            } else {
                startTimer();
            }
        });

        enableCarousel();
        startTimer();
    });
});

/* =========================================
   SAFE SCROLL REVEAL ANIMATIONS
   Reddy's Real Estate
   ========================================= */

document.addEventListener("DOMContentLoaded", function () {
    const reducedMotion = window.matchMedia(
        "(prefers-reduced-motion: reduce)"
    );

    // Keep everything visible if animations are disabled
    // or the browser does not support IntersectionObserver.
            if (
        reducedMotion.matches ||
        !("IntersectionObserver" in window)
    ) {
        return;
    }

    const selectors = [
        ".hero-text",
        ".hero-stats",
        ".section-header",
        ".category",
        ".featured .property-card",
        ".why-card",
        ".listing-page .property-card",
        ".detail-container",
        ".contact-container",
        ".register-wrapper",
        ".dashboard-welcome",
        ".dashboard-stats > *",
        ".footer-container > *"
    ];

    const elements = new Set();

    selectors.forEach(function (selector) {
        document.querySelectorAll(selector).forEach(function (element) {
            elements.add(element);
        });
    });

    if (elements.size === 0) return;

    const observer = new IntersectionObserver(
        function (entries) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-in-view");
                } else {
                    // Allow the animation to replay when scrolling back.
                    entry.target.classList.remove("is-in-view");
                }
            });
        },
                {
            threshold: 0.01,
            rootMargin: "0px 0px 12% 0px"
        }
    );

    // Prepare elements before enabling the animation styles.
    elements.forEach(function (element) {
        element.classList.add("re-scroll-animate");
        observer.observe(element);
    });

    document.documentElement.classList.add(
        "re-scroll-animations-ready"
    );
});                                                                               
