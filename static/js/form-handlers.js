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
});
