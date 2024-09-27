// Simulate server response function
function simulateServerResponse(userData) {
    // Simulated response after a delay
    return new Promise((resolve) => {
        setTimeout(() => {
            resolve(`Thank you, ${userData.name}! Your request for ${userData.emergencyType} has been received. We will contact you shortly at ${userData.phone}.`);
        }, 2000); // Simulate a 2-second response time
    });
}

// JavaScript to handle emergency type selection
document.getElementById('emergencyType').addEventListener('change', function() {
    const naturalDisasterOptions = document.getElementById('naturalDisasterOptions');
    const medicalServicesOptions = document.getElementById('medicalServicesOptions');
    const otherOptions = document.getElementById('otherOptions');

    // Hide all options initially
    naturalDisasterOptions.classList.add('hidden');
    medicalServicesOptions.classList.add('hidden');
    otherOptions.classList.add('hidden');

    // Show relevant options based on selection
    if (this.value === 'naturalDisaster') {
        naturalDisasterOptions.classList.remove('hidden');
    } else if (this.value === 'medicalServices') {
        medicalServicesOptions.classList.remove('hidden');
    } else if (this.value === 'other') {
        otherOptions.classList.remove('hidden');
    }
});

// Handle form submission
document.getElementById('assistanceForm').addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Collect form data
    const name = document.getElementById('name').value;
    const phone = document.getElementById('phone').value;
    const email = document.getElementById('email').value;
    const emergencyType = document.getElementById('emergencyType').value;
    let details = '';

    // Gather additional details based on emergency type
    if (emergencyType === 'naturalDisaster') {
        const medicine = document.querySelector('input[value="medicine"]').checked ? 'Medicine' : '';
        const food = document.querySelector('input[value="food"]').checked ? 'Food' : '';
        const shelter = document.querySelector('input[value="shelter"]').checked ? 'Shelter' : '';
        details = `Requested Resources: ${[medicine, food, shelter].filter(Boolean).join(', ')}`;
    } else if (emergencyType === 'medicalServices') {
        const medicalNeeded = document.querySelector('input[value="yes"]').checked ? 'Yes' : 'No';
        details = `Medical Services Needed: ${medicalNeeded}`;
    } else if (emergencyType === 'other') {
        details = document.getElementById('otherMessage').value;
    }

    // Display confirmation message
    alert(`Request Submitted!\nName: ${name}\nPhone: ${phone}\nEmail: ${email}\nEmergency Type: ${emergencyType}\nDetails: ${details}`);

    // Simulate sending request to the server and getting a response
    const feedbackMessage = await simulateServerResponse({ name, phone, emergencyType });
    alert(feedbackMessage); // Display feedback from the "server"

    this.reset(); // Reset the form after submission
});
