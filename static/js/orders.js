// DEBUG: Check if ORDERS_API is available
console.log('🔍 ORDERS.js LOADED - ORDERS_API:', typeof ORDERS_API !== 'undefined' ? ORDERS_API : 'UNDEFINED');

// If ORDERS_API is undefined, define it temporarily
if (typeof ORDERS_API === 'undefined') {
    console.error('❌ ORDERS_API is undefined! Script loading order issue.');
    const ORDERS_API = window.location.origin + '/api/orders';
    console.log('🔧 TEMPORARY FIX: Defined ORDERS_API as:', ORDERS_API);
}

// Order Functions
async function loadOrders() {
    const token = localStorage.getItem('access_token');
    const loadingElement = document.getElementById('ordersLoading');
    const listElement = document.getElementById('ordersList');
    
    console.log('🔐 DEBUG: Token exists:', !!token);
    console.log('📡 DEBUG: ORDERS_API:', ORDERS_API);
    console.log('📡 DEBUG: Calling URL:', `${ORDERS_API}/`);
    
    if (!token) {
        console.log('❌ DEBUG: No token, redirecting to login');
        navigateTo('/login');
        return;
    }

    loadingElement.classList.remove('hidden');
    listElement.innerHTML = '';

    try {
        console.log('🚀 DEBUG: Making API request to orders...');
        const response = await fetch(`${ORDERS_API}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        console.log('📊 DEBUG: Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📦 DEBUG: Raw orders data:', data);
            
            // FIX: Handle both array and paginated response formats
            let orders = [];
            if (Array.isArray(data)) {
                orders = data;
            } else if (data.results && Array.isArray(data.results)) {
                orders = data.results; // Paginated response
            } else {
                console.error('❌ Unexpected orders format:', data);
                orders = [];
            }
            
            console.log('✅ DEBUG: Processed orders:', orders);
            displayOrders(orders);
        } else {
            console.error('❌ DEBUG: API Error - Status:', response.status);
            const errorText = await response.text();
            console.error('❌ DEBUG: Error response:', errorText);
            listElement.innerHTML = `<div class="error">❌ Error loading orders (${response.status})</div>`;
        }
    } catch (error) {
        console.error('❌ DEBUG: Network error:', error);
        listElement.innerHTML = `<div class="error">❌ Error loading orders: ${error.message}</div>`;
    } finally {
        loadingElement.classList.add('hidden');
    }
}

function displayOrders(orders) {
    const ordersListElement = document.getElementById('ordersList');
    
    // FIX: Check if orders is an array and has items
    if (!orders || !Array.isArray(orders) || orders.length === 0) {
        ordersListElement.innerHTML = '<div class="info"><i class="fas fa-clipboard-list"></i> No orders found</div>';
        return;
    }

    ordersListElement.innerHTML = orders.map(order => `
        <div class="order-item">
            <h4><i class="fas fa-box"></i> Order #${order.order_number}</h4>
            <p><strong>Status:</strong> <span class="status-badge status-${order.status}">${order.status}</span></p>
            <p><strong>Total:</strong> $${order.total_amount}</p>
            <p><strong>Date:</strong> ${new Date(order.created_at).toLocaleDateString()}</p>
            <p><strong>Items:</strong> ${order.total_items}</p>
            <div class="order-actions">
                <button class="btn-secondary" onclick="navigateTo('/order/${order.id}')">
                    <i class="fas fa-eye"></i> View Details
                </button>
                ${order.status === 'delivered' ? `
                    <button class="btn-warning" onclick="requestRefund(${order.id})">
                        <i class="fas fa-money-bill-wave"></i> Request Refund
                    </button>
                    <button class="btn-info" onclick="showReviewForm(${order.id})">
                        <i class="fas fa-star"></i> Write Review
                    </button>
                ` : ''}
                ${order.status === 'pending' ? `
                    <button class="btn-danger" onclick="cancelOrder(${order.id})">
                        <i class="fas fa-times"></i> Cancel Order
                    </button>
                ` : ''}
            </div>
        </div>
    `).join('');
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
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            const order = await response.json();
            displayOrderDetail(order);
        }
    } catch (error) {
        document.getElementById('orderDetailContent').innerHTML = `<div class="error">❌ Error loading order details</div>`;
    }
}

function displayOrderDetail(order) {
    document.getElementById('orderDetailContent').innerHTML = `
        <div class="order-details">
            <div class="flex justify-between items-center mb-6">
                <h2><i class="fas fa-clipboard-list"></i> Order #${order.order_number}</h2>
                <span class="status-badge status-${order.status}">${order.status}</span>
            </div>
            
            <div class="grid-2">
                <div>
                    <h4><i class="fas fa-info-circle"></i> Order Information</h4>
                    <p><strong>Order Date:</strong> ${new Date(order.created_at).toLocaleString()}</p>
                    <p><strong>Total Amount:</strong> $${order.total_amount}</p>
                    <p><strong>Total Items:</strong> ${order.total_items}</p>
                </div>
                <div>
                    <h4><i class="fas fa-home"></i> Shipping Address</h4>
                    <p>${order.shipping_address}</p>
                </div>
            </div>

            <div class="order-items">
                <h4><i class="fas fa-boxes"></i> Order Items</h4>
                ${order.items ? order.items.map(item => `
                    <div class="order-item-detail">
                        <div>
                            <strong>${item.product_name}</strong>
                            <p>Quantity: ${item.quantity}</p>
                        </div>
                        <div class="text-right">
                            <p>$${item.product_price} each</p>
                            <strong>$${(item.product_price * item.quantity).toFixed(2)}</strong>
                        </div>
                    </div>
                `).join('') : '<p>No items found</p>'}
            </div>

            <div class="order-actions">
                <button class="btn-secondary" onclick="navigateTo('/orders')">
                    <i class="fas fa-arrow-left"></i> Back to Orders
                </button>
                ${order.status === 'delivered' ? `
                    <button class="btn-warning" onclick="requestRefund(${order.id})">
                        <i class="fas fa-money-bill-wave"></i> Request Refund
                    </button>
                    <button class="btn-info" onclick="showReviewForm(${order.id})">
                        <i class="fas fa-star"></i> Write Review
                    </button>
                ` : ''}
                ${order.status === 'pending' ? `
                    <button class="btn-danger" onclick="cancelOrder(${order.id})">
                        <i class="fas fa-times"></i> Cancel Order
                    </button>
                ` : ''}
            </div>
        </div>

        ${order.status === 'delivered' ? `
            <div id="reviewSection" class="hidden">
                <div class="review-form">
                    <h4><i class="fas fa-star"></i> Write a Review</h4>
                    <div class="rating-stars">
                        ${[1,2,3,4,5].map(star => `
                            <span class="star" onclick="setRating(${star})">★</span>
                        `).join('')}
                    </div>
                    <div class="form-group">
                        <label>Review Comment:</label>
                        <textarea id="reviewComment" rows="3" placeholder="Share your experience with this product..."></textarea>
                    </div>
                    <button class="btn-success" onclick="submitReview(${order.id})">Submit Review</button>
                    <button class="btn-secondary" onclick="hideReviewForm()">Cancel</button>
                </div>
            </div>
        ` : ''}
    `;
}

// Order Actions
async function requestRefund(orderId) {
    if (!confirm('Are you sure you want to request a refund for this order?')) return;

    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`${ORDERS_API}/${orderId}/refund/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            showMessage('orderDetailContent', '✅ Refund request submitted successfully!', 'success');
            setTimeout(() => {
                loadOrderDetail(orderId);
            }, 2000);
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to request refund');
        }
    } catch (error) {
        showMessage('orderDetailContent', `❌ Error: ${error.message}`, 'error');
    }
}

async function cancelOrder(orderId) {
    if (!confirm('Are you sure you want to cancel this order?')) return;

    const token = localStorage.getItem('access_token');
    try {
        const response = await fetch(`${ORDERS_API}/${orderId}/cancel/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (response.ok) {
            showMessage('orderDetailContent', '✅ Order cancelled successfully!', 'success');
            setTimeout(() => {
                loadOrderDetail(orderId);
            }, 2000);
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to cancel order');
        }
    } catch (error) {
        showMessage('orderDetailContent', `❌ Error: ${error.message}`, 'error');
    }
}

// Review Functions
let currentRating = 0;

function showReviewForm(orderId) {
    currentOrderId = orderId;
    document.getElementById('reviewSection').classList.remove('hidden');
}

function hideReviewForm() {
    document.getElementById('reviewSection').classList.add('hidden');
    currentRating = 0;
    updateStars();
}

function setRating(rating) {
    currentRating = rating;
    updateStars();
}

function updateStars() {
    const stars = document.querySelectorAll('.star');
    stars.forEach((star, index) => {
        if (index < currentRating) {
            star.classList.add('active');
        } else {
            star.classList.remove('active');
        }
    });
}

async function submitReview(orderId) {
    const token = localStorage.getItem('access_token');
    const comment = document.getElementById('reviewComment').value;

    if (currentRating === 0) {
        showMessage('reviewSection', '❌ Please select a rating', 'error');
        return;
    }

    try {
        // Get the order details first
        const orderResponse = await fetch(`${ORDERS_API}/${orderId}/`, {
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        });

        if (!orderResponse.ok) {
            throw new Error('Failed to fetch order details');
        }

        const order = await orderResponse.json();
        
        // Extract product ID from the order items
        let productId = null;
        
        if (order.items && order.items.length > 0) {
            // Try to get product ID from the first item
            const firstItem = order.items[0];
            
            // Check all possible field names where product ID might be stored
            if (firstItem.product_id) {
                productId = firstItem.product_id;
            } else if (firstItem.product && firstItem.product.id) {
                productId = firstItem.product.id;
            } else if (firstItem.product) {
                productId = firstItem.product;
            } else if (firstItem.id) {
                productId = firstItem.id;
            }
        }

        if (!productId) {
            throw new Error('Could not find product ID in order. Please contact support.');
        }

        // Submit the review
        const response = await fetch(`${REVIEWS_API}/`, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                product_id: parseInt(productId),
                rating: currentRating,
                comment: comment
            })
        });

        const data = await response.json();

        if (response.ok) {
            showMessage('reviewSection', '✅ Review submitted successfully!', 'success');
            hideReviewForm();
        } else {
            throw new Error(data.detail || data.error || 'Failed to submit review');
        }
    } catch (error) {
        console.error('Review submission error:', error);
        showMessage('reviewSection', `❌ Error: ${error.message}`, 'error');
    }
}

// View order details
function viewOrderDetails(orderId) {
    navigateTo(`/order/${orderId}`);
}