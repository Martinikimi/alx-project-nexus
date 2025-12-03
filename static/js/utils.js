// ====== API CONFIGURATION  ======
const IS_LOCAL = window.location.hostname === 'localhost' || 
                 window.location.hostname === '127.0.0.1';

const API_BASE_URL = IS_LOCAL 
    ? 'http://127.0.0.1:8000' 
    : 'https://alx-project-nexus-agn5.onrender.com';

// API Endpoints
const API_BASE = `${API_BASE_URL}/api`;
const AUTH_API = `${API_BASE}/auth`;
const PRODUCTS_API = `${API_BASE}/products`;
const CATEGORIES_API = `${API_BASE}/categories`;
const CART_API = `${API_BASE}/cart`;
const ORDERS_API = `${API_BASE}/orders`;
const PAYMENTS_API = `${API_BASE}/payments`;
const REVIEWS_API = `${API_BASE}/reviews`;

console.log('🌐 App initialized');
console.log('📍 Running on:', IS_LOCAL ? 'Localhost' : 'Render');
console.log('🚀 API Base URL:', API_BASE_URL);

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

let paginationState = {
    currentPage: 1,
    pageSize: 15,
    totalPages: 1,
    totalCount: 0,
    hasNext: false,
    hasPrevious: false
};

// Utility Functions
function showMessage(containerId, message, type) {
    const container = document.getElementById(containerId);
    if (!container) {
        console.warn(`Container ${containerId} not found for message:`, message);
        return;
    }
    
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
    if (!backToTopButton) return;
    
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
        const el = document.getElementById(section);
        if (el) el.classList.add('hidden');
    });

    // Show the correct section based on URL
    switch(path) {
        case '/':
            document.getElementById('homePage')?.classList.remove('hidden');
            if (typeof loadFeaturedProducts === 'function') loadFeaturedProducts();
            break;
        case '/login':
            document.getElementById('loginForm')?.classList.remove('hidden');
            break;
        case '/register':
            document.getElementById('registerForm')?.classList.remove('hidden');
            break;
        case '/profile':
            document.getElementById('profileSection')?.classList.remove('hidden');
            if (typeof loadProfile === 'function') loadProfile();
            break;
        case '/products':
            document.getElementById('productsPage')?.classList.remove('hidden');
            if (typeof loadProducts === 'function') loadProducts();
            break;
        case '/categories':
            document.getElementById('categoriesPage')?.classList.remove('hidden');
            if (typeof loadCategories === 'function') loadCategories();
            break;
        case '/cart':
            document.getElementById('cartPage')?.classList.remove('hidden');
            if (typeof loadCart === 'function') loadCart();
            break;
        case '/checkout':
            document.getElementById('checkoutPage')?.classList.remove('hidden');
            if (typeof loadCheckoutSummary === 'function') loadCheckoutSummary();
            break;
        case '/orders':
            document.getElementById('ordersPage')?.classList.remove('hidden');
            if (typeof loadOrders === 'function') loadOrders();
            break;
        default:
            if (path.startsWith('/product/')) {
                document.getElementById('productDetailPage')?.classList.remove('hidden');
                const productId = path.split('/')[2];
                if (typeof loadProductDetail === 'function') loadProductDetail(productId);
            } else if (path.startsWith('/order/')) {
                document.getElementById('orderDetailPage')?.classList.remove('hidden');
                const orderId = path.split('/')[2];
                if (typeof loadOrderDetail === 'function') loadOrderDetail(orderId);
            } else {
                document.getElementById('homePage')?.classList.remove('hidden');
                if (typeof loadFeaturedProducts === 'function') loadFeaturedProducts();
            }
    }

    updateNavigation();
}

// Navigation
function updateNavigation() {
    const token = localStorage.getItem('access_token');
    const authLinks = document.getElementById('authLinks');
    const userLinks = document.getElementById('userLinks');
    
    if (authLinks && userLinks) {
        if (token) {
            authLinks.classList.add('hidden');
            userLinks.classList.remove('hidden');
        } else {
            authLinks.classList.remove('hidden');
            userLinks.classList.add('hidden');
        }
    }
    
    // Update cart count
    if (typeof updateCartCount === 'function') updateCartCount();
}

// Handle browser back/forward buttons
window.addEventListener('popstate', function() {
    showSectionForPath(window.location.pathname);
});

// Initialize app
document.addEventListener('DOMContentLoaded', function() {
    console.log('🚀 DOM loaded - Initializing app...');
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
    if (token && typeof loadCart === 'function') {
        loadCart();
    }

    // Add scroll event listener for back-to-top button
    window.addEventListener('scroll', updateBackToTopButton);
    
    console.log('✅ App initialized successfully');
});

// Authentication Functions 
async function handleLogin(e) {
    if (e) e.preventDefault();
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
            showMessage('loginMessage', ' ✅ Login successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('loginMessage', ` ❌ Error: ${data.detail || data.error || JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        console.error('Login error:', error);
        showMessage('loginMessage', ` ❌ Network error: ${error.message}`, 'error');
    }
}

async function handleRegister(e) {
    if (e) e.preventDefault();
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
        showMessage('registerMessage', ' ❌ Passwords do not match!', 'error');
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
            showMessage('registerMessage', ' ✅ Registration successful!', 'success');
            
            setTimeout(() => {
                navigateTo('/');
            }, 1000);
        } else {
            showMessage('registerMessage', ` ❌ Error: ${JSON.stringify(data)}`, 'error');
        }
    } catch (error) {
        console.error('Register error:', error);
        showMessage('registerMessage', ` ❌ Network error: ${error.message}`, 'error');
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
            const profileElement = document.getElementById('profileData');
            if (profileElement) {
                profileElement.innerHTML = `
                    <div class="grid-2">
                        <div class="form-group">
                            <label><i class="fas fa-envelope"></i> Email:</label>
                            <input type="email" value="${userData.email || ''}" readonly>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-user"></i> Username:</label>
                            <input type="text" value="${userData.username || ''}" readonly>
                        </div>
                    </div>
                    <div class="grid-2">
                        <div class="form-group">
                            <label><i class="fas fa-user"></i> First Name:</label>
                            <input type="text" value="${userData.first_name || ''}" readonly>
                        </div>
                        <div class="form-group">
                            <label><i class="fas fa-user"></i> Last Name:</label>
                            <input type="text" value="${userData.last_name || ''}" readonly>
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
            }
        } else {
            await refreshToken();
            loadProfile();
        }
    } catch (error) {
        console.error('Error loading profile:', error);
        const profileElement = document.getElementById('profileData');
        if (profileElement) {
            profileElement.innerHTML = `<div class="error">❌ Error loading profile</div>`;
        }
    }
}

async function logout() {
    const refreshToken = localStorage.getItem('refresh_token');
    const token = localStorage.getItem('access_token');
    
    try {
        if (token && refreshToken) {
            await fetch(`${AUTH_API}/logout/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${token}`
                },
                body: JSON.stringify({ refresh: refreshToken })
            });
        }
    } catch (error) {
        console.error('Logout error:', error);
    } finally {
        localStorage.removeItem('access_token');
        localStorage.removeItem('refresh_token');
        navigateTo('/login');
    }
}

// Cart Functions
async function loadCart() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        const cartItems = document.getElementById('cartItems');
        if (cartItems) {
            cartItems.innerHTML = '<div class="warning">Please login to view your cart</div>';
        }
        cart = { items: [], cart_total: 0, total_items: 0 };
        updateCartCount();
        return;
    }

    try {
        const response = await fetch(`${CART_API}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            cart = await response.json();
            updateCartCount();
            const cartPage = document.getElementById('cartPage');
            if (cartPage && !cartPage.classList.contains('hidden')) {
                displayCart();
            }
        }
    } catch (error) {
        console.error('Error loading cart:', error);
        const cartItems = document.getElementById('cartItems');
        if (cartItems) {
            cartItems.innerHTML = '<div class="error">❌ Error loading cart</div>';
        }
    }
}

function displayCart() {
    const cartItemsElement = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');

    if (!cart || !cart.items || cart.items.length === 0) {
        if (cartItemsElement) {
            cartItemsElement.innerHTML = '<div class="info"><i class="fas fa-shopping-cart"></i> Your cart is empty</div>';
        }
        if (cartTotalElement) {
            cartTotalElement.innerHTML = '';
        }
        return;
    }

    if (cartItemsElement) {
        cartItemsElement.innerHTML = cart.items.map(item => `
            <div class="cart-item">
                <h4>${item.product_name || 'Product'}</h4>
                <p><i class="fas fa-dollar-sign"></i> Price: $${item.product_price || 0}</p>
                <div class="quantity-controls">
                    <button class="btn-secondary quantity-btn" onclick="updateCartItem(${item.id}, ${item.quantity - 1})">-</button>
                    <span class="quantity-display">${item.quantity || 0}</span>
                    <button class="btn-secondary quantity-btn" onclick="updateCartItem(${item.id}, ${item.quantity + 1})">+</button>
                </div>
                <p><i class="fas fa-receipt"></i> Total: $${item.item_total || 0}</p>
                <button class="btn-danger" onclick="removeCartItem(${item.id})">
                    <i class="fas fa-trash"></i> Remove
                </button>
            </div>
        `).join('');
    }

    if (cartTotalElement) {
        cartTotalElement.innerHTML = `
            <div class="success">
                <h3><i class="fas fa-receipt"></i> Cart Total: $${cart.cart_total || 0}</h3>
                <p><i class="fas fa-box"></i> Total Items: ${cart.total_items || 0}</p>
            </div>
        `;
    }
}

function updateCartCount() {
    const cartCountElement = document.getElementById('cartCount');
    if (cartCountElement) {
        if (cart && cart.total_items > 0) {
            cartCountElement.textContent = cart.total_items;
            cartCountElement.classList.remove('hidden');
        } else {
            cartCountElement.classList.add('hidden');
        }
    }
}

async function addToCart(productId) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showMessage('productsPage', ' ⚠️ Please login to add items to cart', 'warning');
        navigateTo('/login');
        return;
    }

    try {
        const response = await fetch(`${CART_API}/add/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: productId,
                quantity: 1
            })
        });

        if (response.ok) {
            await loadCart();
            showMessage('productsPage', ' ✅ Product added to cart!', 'success');
        } else {
            const errorData = await response.json();
            throw new Error(errorData.error || 'Failed to add to cart');
        }
    } catch (error) {
        console.error('Add to cart error:', error);
        showMessage('productsPage', ` ❌ Error adding to cart: ${error.message}`, 'error');
    }
}

async function updateCartItem(itemId, newQuantity) {
    if (newQuantity < 1) {
        removeCartItem(itemId);
        return;
    }

    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`${CART_API}/items/${itemId}/update/`, {
            method: 'PATCH',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                quantity: newQuantity
            })
        });

        if (response.ok) {
            await loadCart();
        } else {
            throw new Error('Failed to update cart item');
        }
    } catch (error) {
        console.error('Error updating cart item:', error);
        showMessage('cartPage', '❌ Error updating quantity', 'error');
    }
}

async function removeCartItem(itemId) {
    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`${CART_API}/items/${itemId}/remove/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            await loadCart();
            displayCart();
            showMessage('cartPage', '✅ Item removed from cart', 'success');
        } else {
            throw new Error('Failed to remove item');
        }
    } catch (error) {
        console.error('Error removing cart item:', error);
        showMessage('cartPage', ' ❌ Error removing item', 'error');
    }
}

async function clearCart() {
    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`${CART_API}/clear/`, {
            method: 'DELETE',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            await loadCart();
            displayCart();
            showMessage('cartPage', ' ✅ Cart cleared successfully', 'success');
        } else {
            throw new Error('Failed to clear cart');
        }
    } catch (error) {
        console.error('Error clearing cart:', error);
        showMessage('cartPage', ' ❌ Error clearing cart', 'error');
    }
}

// Checkout Functions
function loadCheckoutSummary() {
    const summaryElement = document.getElementById('checkoutSummary');
    if (!summaryElement) return;
    
    if (!cart || !cart.items || cart.items.length === 0) {
        summaryElement.innerHTML = '<div class="warning"><i class="fas fa-shopping-cart"></i> Your cart is empty</div>';
        return;
    }

    summaryElement.innerHTML = `
        <div class="info">
            <h4><i class="fas fa-clipboard-list"></i> Order Summary</h4>
            <p>Total Items: ${cart.total_items || 0}</p>
            <p>Total Amount: $${cart.cart_total || 0}</p>
        </div>
    `;
}

// Order Creation
document.addEventListener('DOMContentLoaded', function() {
    const checkoutForm = document.getElementById('checkoutForm');
    if (checkoutForm) {
        checkoutForm.addEventListener('submit', async function(e) {
            e.preventDefault();
            
            const token = localStorage.getItem('access_token');
            const shippingAddress = document.getElementById('shippingAddress')?.value;

            if (!cart || !cart.items || cart.items.length === 0) {
                showMessage('checkoutMessage', '❌ Your cart is empty', 'error');
                return;
            }

            try {
                const response = await fetch(`${ORDERS_API}/create/`, {
                    method: 'POST',
                    headers: {
                        'Authorization': `Bearer ${token}`,
                        'Content-Type': 'application/json',
                    },
                    body: JSON.stringify({
                        shipping_address: shippingAddress || 'Not provided'
                    })
                });

                if (response.ok) {
                    const data = await response.json();
                    showMessage('checkoutMessage', ` ✅ Order created successfully! Order #${data.order_number}`, 'success');
                    await loadCart();
                    setTimeout(() => {
                        navigateTo('/orders');
                    }, 2000);
                } else {
                    const error = await response.json();
                    throw new Error(error.error || 'Failed to create order');
                }
            } catch (error) {
                showMessage('checkoutMessage', ` ❌ Error: ${error.message}`, 'error');
            }
        });
    }
});

// MISSING FUNCTION IMPLEMENTATIONS 
async function loadFeaturedProducts() {
    try {
        const response = await fetch(`${PRODUCTS_API}/?is_featured=true&page_size=4`);
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

// Register global functions
window.navigateTo = navigateTo;
window.showMessage = showMessage;
window.loadCart = loadCart;
window.displayCart = displayCart;
window.addToCart = addToCart;
window.updateCartItem = updateCartItem;
window.removeCartItem = removeCartItem;
window.clearCart = clearCart;
window.updateCartCount = updateCartCount;
window.loadCheckoutSummary = loadCheckoutSummary;
window.loadOrders = loadOrders;
window.loadProductDetail = loadProductDetail;
window.loadOrderDetail = loadOrderDetail;
window.loadProfile = loadProfile;
window.logout = logout;
window.handleLogin = handleLogin;
window.handleRegister = handleRegister;
window.refreshToken = refreshToken;
window.scrollToTop = scrollToTop;

console.log('✅ All utility functions registered globally');