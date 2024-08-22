function calculateAge(dob) {
    var today = new Date();
    var parts = dob.split('/');
    // Parse the date from dd/mm/yyyy format
    var birthDate = new Date(parts[2], parts[1] - 1, parts[0]);
    var age = today.getFullYear() - birthDate.getFullYear();
    var monthDiff = today.getMonth() - birthDate.getMonth();
    if (monthDiff < 0 || (monthDiff === 0 && today.getDate() < birthDate.getDate())) {
        age--;
    }
    return age;
}

function updateAge() {
    var dobInput = document.getElementById("id_dob");
    var ageInput = document.getElementById("id_age");
    if (dobInput.value) {
        var age = calculateAge(dobInput.value);
        ageInput.value = age;
    } else {
        ageInput.value = "";
    }
}

window.onload = function() {
    var dobInput = document.getElementById("id_dob");
    dobInput.addEventListener("input", updateAge);
}
