// Cart Functions
async function loadCart() {
    const token = localStorage.getItem('access_token');
    if (!token) {
        document.getElementById('cartItems').innerHTML = '<div class="warning">Please login to view your cart</div>';
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
            if (document.getElementById('cartPage').classList.contains('hidden') === false) {
                displayCart();
            }
        }
    } catch (error) {
        console.error('Error loading cart:', error);
        document.getElementById('cartItems').innerHTML = '<div class="error">❌ Error loading cart</div>';
    }
}

function displayCart() {
    const cartItemsElement = document.getElementById('cartItems');
    const cartTotalElement = document.getElementById('cartTotal');

    if (!cart || cart.items.length === 0) {
        cartItemsElement.innerHTML = '<div class="info"><i class="fas fa-shopping-cart"></i> Your cart is empty</div>';
        cartTotalElement.innerHTML = '';
        return;
    }

    cartItemsElement.innerHTML = cart.items.map(item => `
        <div class="cart-item">
            <h4>${item.product_name}</h4>
            <p><i class="fas fa-dollar-sign"></i> Price: $${item.product_price}</p>
            <div class="quantity-controls">
                <button class="btn-secondary quantity-btn" onclick="updateCartItem(${item.id}, ${item.quantity - 1})">-</button>
                <span class="quantity-display">${item.quantity}</span>
                <button class="btn-secondary quantity-btn" onclick="updateCartItem(${item.id}, ${item.quantity + 1})">+</button>
            </div>
            <p><i class="fas fa-receipt"></i> Total: $${item.item_total}</p>
            <button class="btn-danger" onclick="removeCartItem(${item.id})">
                <i class="fas fa-trash"></i> Remove
            </button>
        </div>
    `).join('');

    cartTotalElement.innerHTML = `
        <div class="success">
            <h3><i class="fas fa-receipt"></i> Cart Total: $${cart.cart_total}</h3>
            <p><i class="fas fa-box"></i> Total Items: ${cart.total_items}</p>
        </div>
    `;
}

function updateCartCount() {
    const cartCountElement = document.getElementById('cartCount');
    if (cart && cart.total_items > 0) {
        cartCountElement.textContent = cart.total_items;
        cartCountElement.classList.remove('hidden');
    } else {
        cartCountElement.classList.add('hidden');
    }
}

async function addToCart(productId) {
    const token = localStorage.getItem('access_token');
    if (!token) {
        showMessage('productsPage', ' Please login to add items to cart', 'warning');
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
            showMessage('productsPage', ' Product added to cart!', 'success');
        } else {
            throw new Error('Failed to add to cart');
        }
    } catch (error) {
        showMessage('productsPage', ' Error adding to cart', 'error');
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
            showMessage('cartPage', 'Item removed from cart', 'success');
        }
    } catch (error) {
        console.error('Error removing cart item:', error);
        showMessage('cartPage', ' Error removing item', 'error');
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
            showMessage('cartPage', ' Cart cleared successfully', 'success');
        }
    } catch (error) {
        console.error('Error clearing cart:', error);
        showMessage('cartPage', ' Error clearing cart', 'error');
    }
}

// Checkout Functions
function loadCheckoutSummary() {
    const summaryElement = document.getElementById('checkoutSummary');
    if (!cart || cart.items.length === 0) {
        summaryElement.innerHTML = '<div class="warning"><i class="fas fa-shopping-cart"></i> Your cart is empty</div>';
        return;
    }

    summaryElement.innerHTML = `
        <div class="info">
            <h4><i class="fas fa-clipboard-list"></i> Order Summary</h4>
            <p>Total Items: ${cart.total_items}</p>
            <p>Total Amount: $${cart.cart_total}</p>
        </div>
    `;
}

// Order Creation
document.getElementById('checkoutForm').addEventListener('submit', async function(e) {
    e.preventDefault();
    
    const token = localStorage.getItem('access_token');
    const shippingAddress = document.getElementById('shippingAddress').value;

    if (!cart || cart.items.length === 0) {
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
                shipping_address: shippingAddress
            })
        });

        if (response.ok) {
            const data = await response.json();
            showMessage('checkoutMessage', ` Order created successfully! Order #${data.order_number}`, 'success');
            await loadCart();
            setTimeout(() => {
                navigateTo('/orders');
            }, 2000);
        } else {
            const error = await response.json();
            throw new Error(error.error || 'Failed to create order');
        }
    } catch (error) {
        showMessage('checkoutMessage', ` Error: ${error.message}`, 'error');
    }
});