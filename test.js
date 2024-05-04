// Import Axios library if you're using a module system like ES6 modules
// import axios from 'axios';

// Otherwise, include Axios via CDN in your HTML file:
// <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>

// Define the form data
const formData = new FormData();
formData.append('fullname', 'John Doe');
formData.append('phone', '123456789');
formData.append('email', 'johndoe@example.com');
formData.append('adresse', '123 Main St');
formData.append('profile', 'user');
formData.append('password', 'secretpassword');

// Make a POST request using Axios
axios.post('http://localhost:5000/registre', formData)
  .then(response => {
    // Handle success
    console.log('Response:', response.data);
    // You can do something with the response if needed
  })
  .catch(error => {
    // Handle error
    console.error('Error:', error);
    // You can handle errors here, such as displaying an error message to the user
  });
