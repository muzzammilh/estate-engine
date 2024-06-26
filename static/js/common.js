document.addEventListener("DOMContentLoaded", function() {
    // Check local storage for sidebar state
    if (localStorage.getItem("sidebarState") === "shrink") {
        document.querySelector("#sidebar").classList.add("shrink");
    } else {
        document.querySelector("#sidebar").classList.add("expand");
    }

    // Toggle button click event
    const hamBurger = document.querySelector(".toggle-btn");
    hamBurger.addEventListener("click", function() {
        const sidebar = document.querySelector("#sidebar");
        sidebar.classList.toggle("shrink");
        sidebar.classList.toggle("expand");

        // Save the current state to local storage
        if (sidebar.classList.contains("shrink")) {
            localStorage.setItem("sidebarState", "shrink");
        } else {
            localStorage.setItem("sidebarState", "expand");
        }
    });
});
