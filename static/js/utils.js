// API Base URLs
const API_BASE = 'http://127.0.0.1:8000/api';
const AUTH_API = `${API_BASE}/auth`;
const PRODUCTS_API = `${API_BASE}/products`;
const CATEGORIES_API = `${API_BASE}/categories`;
const CART_API = `${API_BASE}/cart`;
const ORDERS_API = `${API_BASE}/orders`;
const PAYMENTS_API = `${API_BASE}/payments`;
const REVIEWS_API = `${API_BASE}/reviews/create`;

// Global state
let currentUser = null;
let cart = null;
let products = [];
let categories = [];
let currentOrderId = null;
let currentFilters = {
    search: '',
    category: '',
    minPrice: '',
    maxPrice: '',
    sort: ''
};

// FIXED: Global state with proper initialization
let paginationState = {
    currentPage: 1,
    pageSize: 15, // Default value
    totalPages: 1,
    totalCount: 0,
    hasNext: false,
    hasPrevious: false
};

// Utility Functions
function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    const existingMessage = container.querySelector('.error, .success, .info, .warning');
    if (existingMessage) {
        existingMessage.remove();
    }
    
    const messageElement = document.createElement('div');
    messageElement.className = type;
    messageElement.innerHTML = message;
    container.insertBefore(messageElement, container.firstChild);

    if (type === 'success') {
        setTimeout(() => {
            if (messageElement.parentNode) {
                messageElement.remove();
            }
        }, 5000);
    }
}

async function refreshToken() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    try {
        const response = await fetch(`${AUTH_API}/token/refresh/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ refresh: refreshToken })
        });

        if (response.ok) {
            const data = await response.json();
            localStorage.setItem('access_token', data.access);
            return true;
        } else {
            throw new Error('Token refresh failed');
        }
    } catch (error) {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigateTo('/login');
        return false;
    }
}

// Back to Top functionality
function updateBackToTopButton() {
    const backToTopButton = document.querySelector('.back-to-top');
    if (window.scrollY > 300) {
        backToTopButton.classList.add('visible');
    } else {
        backToTopButton.classList.remove('visible');
    }
}

function scrollToTop() {
    window.scrollTo({
        top: 0,
        behavior: 'smooth'
    });
}

// URL Routing System
function navigateTo(path) {
    window.history.pushState({}, '', path);
    showSectionForPath(path);
    updateBackToTopButton();
}

function showSectionForPath(path) {
    // Hide all sections
    const sections = [
        'homePage', 'loginForm', 'registerForm', 'profileSection',
        'productsPage', 'categoriesPage', 'cartPage', 'checkoutPage',
        'ordersPage', 'productDetailPage', 'orderDetailPage'
    ];
    sections.forEach(section => {
        document.getElementById(section).classList.add('hidden');
    });

    // Show the correct section based on URL
    switch(path) {
        case '/':
            document.getElementById('homePage').classList.remove('hidden');
            loadFeaturedProducts();
            break;
        case '/login':
            document.getElementById('loginForm').classList.remove('hidden');
            break;
        case '/register':
            document.getElementById('registerForm').classList.remove('hidden');
            break;
        case '/profile':
            document.getElementById('profileSection').classList.remove('hidden');
            loadProfile();
            break;
        case '/products':
            document.getElementById('productsPage').classList.remove('hidden');
            loadProducts();
            break;
        case '/categories':
            document.getElementById('categoriesPage').classList.remove('hidden');
            loadCategories();
            break;
        case '/cart':
            document.getElementById('cartPage').classList.remove('hidden');
            loadCart();
            break;
        case '/checkout':
            document.getElementById('checkoutPage').classList.remove('hidden');
            loadCheckoutSummary();
            break;
        case '/orders':
            document.getElementById('ordersPage').classList.remove('hidden');
            loadOrders();
            break;
        default:
            if (path.startsWith('/product/')) {
                document.getElementById('productDetailPage').classList.remove('hidden');
                const productId = path.split('/')[2];
                loadProductDetail(productId);
            } else if (path.startsWith('/order/')) {
                document.getElementById('orderDetailPage').classList.remove('hidden');
                const orderId = path.split('/')[2];
                loadOrderDetail(orderId);
            } else {
                document.getElementById('homePage').classList.remove('hidden');
                loadFeaturedProducts();
            }
    }

    updateNavigation();
}

// Navigation
function updateNavigation() {
    const token = localStorage.getItem('access_token');
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');
    
    if (token) {
        authLinks.classList.add('hidden');
        userLinks.classList.remove('hidden');
    } else {
        authLinks.classList.remove('hidden');
        userLinks.classList.add('hidden');
    }
    
    // Update cart count
    updateCartCount();
}

// Handle browser back/forward buttons
window.addEventListener('popstate', function() {
    showSectionForPath(window.location.pathname);
});

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
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