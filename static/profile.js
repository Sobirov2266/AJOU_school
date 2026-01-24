// DOM Elements
const editProfileBtn = document.getElementById('editProfileBtn');
const editProfileModal = document.getElementById('editProfileModal');
const closeModalBtn = document.getElementById('closeModalBtn');
const cancelEditBtn = document.getElementById('cancelEditBtn');
const profileForm = document.getElementById('profileForm');
const notification = document.getElementById('notification');
const changePhotoBtn = document.getElementById('changePhotoBtn');

// Open Edit Profile Modal
editProfileBtn.addEventListener('click', () => {
    editProfileModal.style.display = 'flex';
});

// Close Modal
function closeModal() {
    editProfileModal.style.display = 'none';
}

closeModalBtn.addEventListener('click', closeModal);
cancelEditBtn.addEventListener('click', closeModal);

// Close modal when clicking outside of it
window.addEventListener('click', (event) => {
    if (event.target === editProfileModal) {
        closeModal();
    }
});

// Handle Form Submission
profileForm.addEventListener('submit', (event) => {
    event.preventDefault();

    // In a real application, you would send the data to the server here
    // For this example, we'll just show a notification

    // Get form values
    const fullName = document.getElementById('fullName').value;
    const email = document.getElementById('email').value;
    const phone = document.getElementById('phone').value;
    const address = document.getElementById('address').value;
    const specialization = document.getElementById('specialization').value;
    const education = document.getElementById('education').value;

    // Update the profile info on the page
    document.querySelector('.profile-name').textContent = fullName.split(' ')[0] + ' ' + fullName.split(' ')[1];
    document.querySelector('.user-info span').textContent = fullName.split(' ')[0] + ' ' + fullName.split(' ')[1];

    // Update profile title if specialization changed
    if (specialization) {
        document.querySelector('.profile-title').textContent = specialization;
    }

    // Update details
    document.querySelectorAll('.detail-value')[0].textContent = fullName;
    document.querySelectorAll('.detail-value')[3].textContent = email;
    document.querySelectorAll('.detail-value')[2].textContent = phone;
    document.querySelectorAll('.detail-value')[4].textContent = address;
    document.querySelectorAll('.detail-value')[6].textContent = specialization;
    document.querySelectorAll('.detail-value')[9].textContent = education;

    // Show notification
    notification.style.display = 'block';

    // Close modal
    closeModal();

    // Hide notification after 3 seconds
    setTimeout(() => {
        notification.style.display = 'none';
    }, 3000);
});

// Change Photo Button
changePhotoBtn.addEventListener('click', () => {
    alert("Haqiqiy ilovada bu joyda fayl tanlash oynasi ochiladi. Ushbu demo uchun funksionalilik cheklangan.");
});

// Mobile menu toggle for responsive design
const menuItems = document.querySelectorAll('.menu-item');
menuItems.forEach(item => {
    item.addEventListener('click', () => {
        // Remove active class from all items
        menuItems.forEach(i => i.classList.remove('active'));
        // Add active class to clicked item
        item.classList.add('active');
    });
});

// Add hover effect to skill tags
const skillTags = document.querySelectorAll('.skill-tag');
skillTags.forEach(tag => {
    tag.addEventListener('mouseenter', () => {
        tag.style.transform = 'translateY(-3px)';
        tag.style.boxShadow = '0 5px 10px rgba(0,0,0,0.1)';
    });

    tag.addEventListener('mouseleave', () => {
        tag.style.transform = 'translateY(0)';
        tag.style.boxShadow = 'none';
    });
});

// Initialize the page
document.addEventListener('DOMContentLoaded', () => {
    console.log('Profil sahifasi yuklandi');
});