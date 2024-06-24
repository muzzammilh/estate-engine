// for the toggle of  sidebar
var el = document.getElementById("wrapper");
var toggleButton = document.getElementById("menu-toggle");
toggleButton.onclick = function () {
  el.classList.toggle("toggled");
};
//for the side bar to stay toggleed in on reload
document.addEventListener("DOMContentLoaded", function () {
  var wrapper = document.getElementById("wrapper");
  var toggleButton = document.getElementById("menu-toggle");

  // Check if the sidebar state is saved in local storage
  if (localStorage.getItem("sidebarToggled") === "true") {
    wrapper.classList.add("toggled");
  }

  toggleButton.onclick = function () {
    wrapper.classList.toggle("toggled");

    // Save the sidebar state in local storage
    if (wrapper.classList.contains("toggled")) {
      localStorage.setItem("sidebarToggled", "true");
    } else {
      localStorage.setItem("sidebarToggled", "false");
    }
  };
});
