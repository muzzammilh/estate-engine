document.addEventListener("DOMContentLoaded", function () {
  const form = document.getElementById("message-form");
  const chatBox = document.getElementById("chat-box");

  form.addEventListener("submit", function (event) {
    event.preventDefault();

    const formData = new FormData(form);

    fetch(form.action, {
      method: "POST",
      body: formData,
      headers: {
        "X-Requested-With": "XMLHttpRequest",
        "X-CSRFToken": formData.get("csrfmiddlewaretoken"),
      },
    })
      .then((response) => {
        if (!response.ok) {
          throw new Error("Network response was not ok");
        }
        return response.json();
      })
      .then((data) => {
        if (data.error) {
          console.error("Error:", data.error);
          return;
        }

        const messageDiv = document.createElement("div");
        messageDiv.className = `d-flex mb-3 ${
          data.sender === "me" ? "justify-content-end" : "justify-content-start"
        }`;

        const messageContent = `
                <div class="message p-2 rounded ${
                  data.sender === "me" ? "bg-primary text-white" : "bg-light"
                }">
                    <p class="mb-1">${data.content}</p>
                    <small class="${
                      data.sender === "me" ? "text-white" : "text-muted"
                    }" style="display: block; text-align: ${
          data.sender === "me" ? "right" : "left"
        };">
                        ${data.timestamp}
                    </small>
                </div>
            `;

        messageDiv.innerHTML = messageContent;
        chatBox.appendChild(messageDiv);

        chatBox.scrollTop = chatBox.scrollHeight;

        form.reset();
      })
      .catch((error) => console.error("Error:", error));
  });
});
