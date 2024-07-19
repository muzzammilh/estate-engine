document.addEventListener("DOMContentLoaded", function () {
  const propertyField = document.getElementById("id_property");
  const unitField = document.getElementById("id_unit");

  function updateDropdown(url, field, placeholder) {
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        console.log("Received data:", data);
        field.innerHTML = `<option value="">${placeholder}</option>`;
        data.forEach((item) => {
          console.log("Processing item:", item);
          field.innerHTML += `<option value="${item.id}">${item.unit_number}</option>`;
        });

      });
  }

  propertyField.addEventListener("change", function () {
    const propertyId = this.value;
    if (propertyId) {
      updateDropdown(
        `/property/ajax/load-units/?property_id=${propertyId}`,
        unitField,
        "Select Unit"
      );
    } else {
      unitField.innerHTML = '<option value="">Select Unit</option>';
    }
  });
});
