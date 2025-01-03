// Handle dynamic building selection based on project
document.addEventListener('DOMContentLoaded', function() {
    const projectSelect = document.querySelector('select[name="project"]');
    const buildingSelect = document.querySelector('select[name="building"]');
    const buildingNameInput = document.querySelector('input[name="building_name"]');
    const facilitySelect = document.querySelector('select[name="facility"]');
    const teamSelect = document.querySelector('select[name="team"]');

    if (projectSelect && buildingSelect) {
        projectSelect.addEventListener('change', function() {
            const projectId = this.value;
            if (projectId) {
                fetch(`/api/buildings/${projectId}/`)
                    .then(response => response.json())
                    .then(data => {
                        buildingSelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(building => {
                            buildingSelect.innerHTML += `<option value="${building.id}">${building.name}</option>`;
                        });
                        buildingSelect.disabled = false;
                    });
            } else {
                buildingSelect.innerHTML = '<option value="">---------</option>';
                buildingSelect.disabled = true;
            }
        });
    }

    if (buildingSelect && buildingNameInput) {
        buildingSelect.addEventListener('change', function() {
            const selectedOption = this.options[this.selectedIndex];
            buildingNameInput.value = selectedOption.text || '';
        });
    }

    // Handle dynamic team selection based on facility
    if (facilitySelect && teamSelect) {
        facilitySelect.addEventListener('change', function() {
            const facilityId = this.value;
            if (facilityId) {
                fetch(`/api/teams/${facilityId}/`)
                    .then(response => response.json())
                    .then(data => {
                        teamSelect.innerHTML = '<option value="">---------</option>';
                        data.forEach(team => {
                            teamSelect.innerHTML += `<option value="${team.id}">${team.name}</option>`;
                        });
                        teamSelect.disabled = false;
                    });
            } else {
                teamSelect.innerHTML = '<option value="">---------</option>';
                teamSelect.disabled = true;
            }
        });
    }

    // Format project number as user types
    const projectNumberInput = document.querySelector('input[name="project_number"]');
    if (projectNumberInput) {
        projectNumberInput.addEventListener('input', function() {
            let value = this.value.toUpperCase();
            if (!value.startsWith('PRJ-')) {
                value = 'PRJ-' + value;
            }
            // Format YYYY
            if (value.length > 4) {
                const year = value.substring(4).replace(/\D/g, '');
                if (year.length > 0) {
                    value = `PRJ-${year.padStart(4, '2')}`;
                }
                // Format XXX
                if (year.length >= 4) {
                    const num = value.substring(9).replace(/\D/g, '');
                    if (num.length > 0) {
                        value = `PRJ-${year.substring(0,4)}-${num.padStart(3, '0')}`;
                    }
                }
            }
            this.value = value;
        });
    }
});
