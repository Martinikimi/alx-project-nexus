// API Base URLs - FIXED
const API_BASE = 'https://alx-project-nexus-agn5.onrender.com/api';
const AUTH_API = `${API_BASE}/auth`;
const PRODUCTS_API = `${API_BASE}/products`;
const CATEGORIES_API = `${API_BASE}/categories`;
const CART_API = `${API_BASE}/cart`;
const ORDERS_API = `${API_BASE}/orders`;
const PAYMENTS_API = `${API_BASE}/payments`;
const REVIEWS_API = `${API_BASE}/reviews`;

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
            document.getElementById('registerForm').classList.remove('hidden'); // FIXED: classList not classlist
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

// Authentication Functions - UPDATED with better error handling
async function handleLogin(e) {
    e.preventDefault();
    console.log('Login form submitted');
    
    const formData = {
        email: document.getElementById('loginEmail').value,
        password: document.getElementById('loginPassword').value
    };

    try {
        const response = await fetch(`${AUTH_API}/login/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Login response:', data);

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            showMessage('loginMessage', ' Login successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('loginMessage', ` Error: ${data.detail || data.error || JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('loginMessage', ` Network error: ${error.message}`, 'error');
    }
}

async function handleRegister(e) {
    e.preventDefault();
    console.log('Register form submitted');
    
    const formData = {
        email: document.getElementById('regEmail').value,
        username: document.getElementById('regUsername').value,
        first_name: document.getElementById('regFirstName').value,
        last_name: document.getElementById('regLastName').value,
        phone_number: document.getElementById('regPhone').value,
        date_of_birth: document.getElementById('regDob').value,
        address: document.getElementById('regAddress').value,
        password: document.getElementById('regPassword').value,
        password_confirm: document.getElementById('regPasswordConfirm').value
    };

    if (formData.password !== formData.password_confirm) {
        showMessage('registerMessage', ' Passwords do not match!', 'error');
        return;
    }

    try {
        const response = await fetch(`${AUTH_API}/register/`, {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify(formData)
        });

        const data = await response.json();
        console.log('Register response:', data);

        if (response.ok) {
            localStorage.setItem('access_token', data.access);
            localStorage.setItem('refresh_token', data.refresh);
            showMessage('registerMessage', ' Registration successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('registerMessage', ` Error: ${JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showMessage('registerMessage', ` Network error: ${error.message}`, 'error');
    }
}

// Add event listeners properly
document.addEventListener('DOMContentLoaded', function() {
    // Login form
    const loginForm = document.getElementById('loginFormElement');
    if (loginForm) {
        loginForm.addEventListener('submit', handleLogin);
    }

    // Register form
    const registerForm = document.getElementById('registerFormElement');
    if (registerForm) {
        registerForm.addEventListener('submit', handleRegister);
    }
});

async function loadProfile() {
    const token = localStorage.getItem('access_token');
    
    if (!token) {
        navigateTo('/login');
        return;
    }

    try {
        const response = await fetch(`${AUTH_API}/profile/`, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const userData = await response.json();
            document.getElementById('profileData').innerHTML = `
                <div class="grid-2">
                    <div class="form-group">
                        <label><i class="fas fa-envelope"></i> Email:</label>
                        <input type="email" value="${userData.email}" readonly>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> Username:</label>
                        <input type="text" value="${userData.username}" readonly>
                    </div>
                </div>
                <div class="grid-2">
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> First Name:</label>
                        <input type="text" value="${userData.first_name}" readonly>
                    </div>
                    <div class="form-group">
                        <label><i class="fas fa-user"></i> Last Name:</label>
                        <input type="text" value="${userData.last_name}" readonly>
                    </div>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-phone"></i> Phone:</label>
                    <input type="text" value="${userData.phone_number || 'Not provided'}" readonly>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-birthday-cake"></i> Date of Birth:</label>
                    <input type="text" value="${userData.date_of_birth || 'Not provided'}" readonly>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-home"></i> Address:</label>
                    <textarea rows="3" readonly>${userData.address || 'Not provided'}</textarea>
                </div>
                <div class="form-group">
                    <label><i class="fas fa-calendar-alt"></i> Age:</label>
                    <input type="text" value="${userData.age || 'Not available'}" readonly>
                </div>
            `;
        } else {
            await refreshToken();
            loadProfile();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        document.getElementById('profileData').innerHTML = `<div class="error">❌ Error loading profile</div>`;
    }
}

async function logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    
    try {
        await fetch(`${AUTH_API}/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${localStorage.getItem('access_token')}`
            },
            body: JSON.stringify({ refresh: refreshToken })
        });
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigateTo('/login');
    }
}

// MISSING FUNCTION IMPLEMENTATIONS - ADDED
async function loadFeaturedProducts() {
    try {
        const response = await fetch(`${PRODUCTS_API}/?featured=true`);
        if (response.ok) {
            const data = await response.json();
            products = data.results || data;
            console.log('Loaded featured products:', products.length);
        }
    } catch (error) {
        console.error('Error loading featured products:', error);
    }
}

async function loadProducts() {
    try {
        const queryParams = new URLSearchParams({
            page: paginationState.currentPage,
            page_size: paginationState.pageSize,
            ...currentFilters
        }).toString();
        
        const response = await fetch(`${PRODUCTS_API}/?${queryParams}`);
        if (response.ok) {
            const data = await response.json();
            products = data.results || data;
            console.log('Loaded products:', products.length);
        }
    } catch (error) {
        console.error('Error loading products:', error);
    }
}

async function loadCategories() {
    try {
        const response = await fetch(`${CATEGORIES_API}/`);
        if (response.ok) {
            const data = await response.json();
            categories = data.results || data;
            console.log('Loaded categories:', categories.length);
        }
    } catch (error) {
        console.error('Error loading categories:', error);
    }
}

async function loadCart() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        cart = { items: [], total_price: 0 };
        updateCartCount();
        return;
    }

    try {
        const response = await fetch(`${CART_API}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            cart = await response.json();
            updateCartCount();
        }
    } catch (error) {
        console.error('Error loading cart:', error);
        cart = { items: [], total_price: 0 };
        updateCartCount();
    }
}

function updateCartCount() {
    const cartCount = document.getElementById('cartCount');
    if (cartCount && cart && cart.items) {
        const totalItems = cart.items.reduce((sum, item) => sum + item.quantity, 0);
        cartCount.textContent = totalItems;
        cartCount.style.display = totalItems > 0 ? 'flex' : 'none';
    }
}

async function loadCheckoutSummary() {
    console.log('Loading checkout summary...');
    // Implementation for checkout page
}

async function loadOrders() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        navigateTo('/login');
        return;
    }

    try {
        const response = await fetch(`${ORDERS_API}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const orders = await response.json();
            console.log('Loaded orders:', orders.length);
        }
    } catch (error) {
        console.error('Error loading orders:', error);
    }
}

async function loadProductDetail(productId) {
    try {
        const response = await fetch(`${PRODUCTS_API}/${productId}/`);
        if (response.ok) {
            const product = await response.json();
            console.log('Loaded product detail:', product.name);
        }
    } catch (error) {
        console.error('Error loading product detail:', error);
    }
}

async function loadOrderDetail(orderId) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        navigateTo('/login');
        return;
    }

    try {
        const response = await fetch(`${ORDERS_API}/${orderId}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const order = await response.json();
            console.log('Loaded order detail:', order.order_number);
        }
    } catch (error) {
        console.error('Error loading order detail:', error);
    }
}