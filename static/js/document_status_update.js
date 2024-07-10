document.addEventListener("DOMContentLoaded", function () {
  const forms = document.querySelectorAll(".update-status-form");

  forms.forEach((form) => {
    form.addEventListener("submit", function (event) {
      event.preventDefault(); // Prevent default form submission

      const formData = new FormData(form);
      const documentId = form.getAttribute("data-document-id");
      const url = form.getAttribute("action"); // Use form's action attribute for URL

      fetch(url, {
        method: "POST",
        body: formData,
        headers: {
          "X-Requested-With": "XMLHttpRequest",
          "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
        },
      })
        .then((response) => response.json())
        .then((data) => {
          console.log(data); // Log response data

          // Display the message on the page
          showMessage(data.message);

          // Update dropdown value based on response
          const selectElement = form.querySelector('select[name="status"]');
          selectElement.value = data.new_status; // Update with the new status returned from server
        })
        .catch((error) => {
          console.error("Error:", error);
        });
    });
  });

  // Function to display message dynamically
  function showMessage(message) {
    const messagesDiv = document.querySelector("#messages"); // Assuming you have a messages container

    // Clear existing messages
    messagesDiv.innerHTML = "";

    // Display the message dynamically
    const messageElement = document.createElement("div");
    messageElement.classList.add(
      "alert",
      "alert-dismissible",
      "alert-primary",
      "m-2"
    );
    messageElement.innerHTML = `
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
            ${message}
        `;
    messagesDiv.appendChild(messageElement);
  }
});
