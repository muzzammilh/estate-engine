document.addEventListener('DOMContentLoaded', function () {
    const countryField = document.getElementById('id_country');
    const stateField = document.getElementById('id_state');
    const cityField = document.getElementById('id_city');
    const subLocalityField = document.getElementById('id_sub_locality');

    function updateDropdown(url, field, placeholder) {
        fetch(url)
            .then(response => response.json())
            .then(data => {
                field.innerHTML = `<option value="">${placeholder}</option>`;
                data.forEach(item => {
                    field.innerHTML += `<option value="${item.id}">${item.name}</option>`;
                });
            });
    }

    countryField.addEventListener('change', function () {
        const countryId = this.value;
        if (countryId) {
            updateDropdown(`/property/ajax/load-states/?country_id=${countryId}`, stateField, 'Select State');
        } else {
            stateField.innerHTML = '<option value="">Select State</option>';
            cityField.innerHTML = '<option value="">Select City</option>';
            subLocalityField.innerHTML = '<option value="">Select Sub Locality</option>';
        }
    });

    stateField.addEventListener('change', function () {
        const stateId = this.value;
        if (stateId) {
            updateDropdown(`/property/ajax/load-cities/?state_id=${stateId}`, cityField, 'Select City');
        } else {
            cityField.innerHTML = '<option value="">Select City</option>';
            subLocalityField.innerHTML = '<option value="">Select Sub Locality</option>';
        }
    });

    cityField.addEventListener('change', function () {
        const cityId = this.value;
        if (cityId) {
            updateDropdown(`/property/ajax/load-sub-localities/?city_id=${cityId}`, subLocalityField, 'Select Sub Locality');
        } else {
            subLocalityField.innerHTML = '<option value="">Select Sub Locality</option>';
        }
    });
});
