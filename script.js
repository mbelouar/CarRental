document.addEventListener('DOMContentLoaded', () => {
    const form = document.getElementById('registrationForm');

    form.addEventListener('submit', async (e) => {
        e.preventDefault(); // Prevent default form submission

        const formData = new FormData(form);

        try {
            const response = await fetch('http://localhost:5000/registre', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Network response was not ok.');
            }

            const responseData = await response.json();
            console.log('Registration successful:', responseData);
            // Optionally, you can redirect the user or display a success message
        } catch (error) {
            console.error('Registration error:', error.message);
            // Handle error: display an error message to the user
        }
    });
});
