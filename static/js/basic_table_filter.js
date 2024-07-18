document.addEventListener("DOMContentLoaded", function () {
  const propertyField = document.getElementById("id_property");
  const unitField = document.getElementById("id_unit");

  function updateDropdown(url, field, placeholder) {
    console.log(field)
    console.log(placeholder)
    fetch(url)
      .then((response) => response.json())
      .then((data) => {
        field.innerHTML = `<option value="">${placeholder}</option>`;
        data.forEach((item) => {
          console.log(item)
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
