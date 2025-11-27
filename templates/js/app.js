// Main application file - imports all other modules
// This file should be loaded last in your HTML

// Global event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Initialize the app
    const token = localStorage.getItem('access_token');
    const currentPath = window.location.pathname;
    
    if (token && (currentPath === '/login' || currentPath === '/register')) {
        navigateTo('/');
    } else if (!token && (currentPath === '/profile' || currentPath === '/cart' || currentPath === '/orders' || currentPath === '/checkout')) {
        navigateTo('/login');
    } else {
        showSectionForPath(currentPath);
    }
    
    // Load initial data
    if (token) {
        loadCart();
    }

    // Add scroll event listener for back-to-top button
    window.addEventListener('scroll', updateBackToTopButton);
});

// Handle browser back/forward buttons
window.addEventListener('popstate', function() {
    showSectionForPath(window.location.pathname);
});