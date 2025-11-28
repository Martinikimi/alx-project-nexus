// Product Functions
async function loadFeaturedProducts() {
    try {
        const response = await fetch(`${PRODUCTS_API}/featured/`);
        if (response.ok) {
            const featuredProducts = await response.json();
            displayFeaturedProducts(featuredProducts.slice(0, 4));
        }
    } catch (error) {
        console.error('Error loading featured products:', error);
    }
}

function displayFeaturedProducts(products) {
    const featuredContainer = document.getElementById('featuredProducts');
    if (products.length === 0) {
        featuredContainer.innerHTML = '<div class="info">No featured products available</div>';
        return;
    }

    featuredContainer.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image-container">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-price">$${product.price}</div>
                <div class="product-category"><i class="fas fa-tag"></i> ${product.category_name}</div>
                <div class="product-actions">
                    <button class="btn-primary" onclick="addToCart(${product.id})">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                    <button class="btn-secondary" onclick="navigateTo('/product/${product.id}')">
                        <i class="fas fa-eye"></i> View
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

function displayProducts(products) {
    const gridElement = document.getElementById('productsGrid');
    if (products.length === 0) {
        gridElement.innerHTML = `
            <div class="info w-full text-center">
                <h3>No products found</h3>
                <p>Try adjusting your search criteria or filters</p>
                <button class="btn-secondary mt-2" onclick="clearFilters()">Clear All Filters</button>
            </div>
        `;
        return;
    }

    gridElement.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image-container">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <div class="product-name">${product.name}</div>
                <div class="product-price">$${product.price}</div>
                <div class="product-category"><i class="fas fa-tag"></i> ${product.category_name}</div>
                <div class="product-actions">
                    <button class="btn-primary" onclick="addToCart(${product.id})">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                    <button class="btn-secondary" onclick="navigateTo('/product/${product.id}')">
                        <i class="fas fa-eye"></i> Details
                    </button>
                </div>
            </div>
        </div>
    `).join('');
}

async function loadProductDetail(productId) {
    try {
        const response = await fetch(`${PRODUCTS_API}/${productId}/`);
        if (response.ok) {
            const product = await response.json();
            displayProductDetail(product);
        }
    } catch (error) {
        document.getElementById('productDetail').innerHTML = `<div class="error">❌ Error loading product details</div>`;
    }
}

function displayProductDetail(product) {
    document.getElementById('productDetail').innerHTML = `
        <div class="product-card">
            <div class="product-image-container" style="height: 400px;">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <h2>${product.name}</h2>
                <div class="product-price">$${product.price}</div>
                <p><strong><i class="fas fa-tag"></i> Category:</strong> ${product.category.name}</p>
                <p><strong><i class="fas fa-align-left"></i> Description:</strong> ${product.description}</p>
                <p><strong><i class="fas fa-box"></i> Stock:</strong> ${product.stock_quantity} available</p>
                <div class="flex gap-3 mt-4">
                    <button class="btn-primary" onclick="addToCart(${product.id})">
                        <i class="fas fa-cart-plus"></i> Add to Cart
                    </button>
                    <button class="btn-secondary" onclick="navigateTo('/products')">
                        <i class="fas fa-arrow-left"></i> Back to Products
                    </button>
                </div>
            </div>
        </div>
    `;
}

// Category Functions
async function loadCategories() {
    const loadingElement = document.getElementById('categoriesLoading');
    const listElement = document.getElementById('categoriesList');
    
    loadingElement.classList.remove('hidden');
    listElement.innerHTML = '';

    try {
        const response = await fetch(`${CATEGORIES_API}/`);
        if (response.ok) {
            categories = await response.json();
            displayCategories(categories);
        }
    } catch (error) {
        listElement.innerHTML = `<div class="error">❌ Error loading categories</div>`;
    } finally {
        loadingElement.classList.add('hidden');
    }
}

function displayCategories(categories) {
    const listElement = document.getElementById('categoriesList');
    if (categories.length === 0) {
        listElement.innerHTML = '<div class="info">No categories found</div>';
        return;
    }

    listElement.innerHTML = categories.map(category => `
        <div class="product-card">
            <div class="product-info">
                <h3><i class="fas fa-tags"></i> ${category.name}</h3>
                <p class="product-category">${category.description || 'No description available'}</p>
                <button class="btn-secondary" onclick="navigateTo('/products')">
                    <i class="fas fa-eye"></i> View Products
                </button>
            </div>
        </div>
    `).join('');
}

// Search and Filter Functions
function handleGlobalSearch(event) {
    if (event.key === 'Enter') {
        performGlobalSearch();
    }
}

function performGlobalSearch() {
    const searchQuery = document.getElementById('globalSearch').value.trim();
    if (searchQuery) {
        currentFilters.search = searchQuery;
        navigateTo('/products');
        setTimeout(() => {
            if (document.getElementById('searchInput')) {
                document.getElementById('searchInput').value = searchQuery;
                applyFilters();
            }
        }, 100);
    }
}

function handleSearchEnter(event) {
    if (event.key === 'Enter') {
        applyFilters();
    }
}

async function loadCategoriesForFilter() {
    try {
        const response = await fetch(`${CATEGORIES_API}/`);
        if (response.ok) {
            const categories = await response.json();
            const categorySelect = document.getElementById('categoryFilter');
            categorySelect.innerHTML = '<option value="">All Categories</option>' +
                categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
            
            if (currentFilters.category) {
                categorySelect.value = currentFilters.category;
            }
        }
    } catch (error) {
        console.error('Error loading categories for filter:', error);
    }
}

function applyFilters() {
    currentFilters = {
        search: document.getElementById('searchInput').value,
        category: document.getElementById('categoryFilter').value,
        minPrice: document.getElementById('minPrice').value,
        maxPrice: document.getElementById('maxPrice').value,
        sort: document.getElementById('sortOption').value
    };
    paginationState.currentPage = 1;
    loadProductsWithFilters();
}

function clearFilters() {
    document.getElementById('searchInput').value = '';
    document.getElementById('categoryFilter').value = '';
    document.getElementById('minPrice').value = '';
    document.getElementById('maxPrice').value = '';
    document.getElementById('sortOption').value = '';
    currentFilters = {
        search: '',
        category: '',
        minPrice: '',
        maxPrice: '',
        sort: ''
    };
    paginationState.currentPage = 1;
    loadProductsWithFilters();
}

function changePageSize(newSize) {
    const size = parseInt(newSize);
    if (!isNaN(size) && size > 0) {
        paginationState.pageSize = size;
        paginationState.currentPage = 1;
        loadProductsWithFilters();
    }
}

// Pagination Functions
function goToPage(pageNumber) {
    const page = parseInt(pageNumber);
    if (!isNaN(page) && page >= 1 && page <= paginationState.totalPages) {
        paginationState.currentPage = page;
        loadProductsWithFilters();
        window.scrollTo({ top: 0, behavior: 'smooth' });
    }
}

function renderPaginationControls() {
    const paginationContainer = document.getElementById('paginationContainer');
    const paginationInfo = document.getElementById('paginationInfo');
    const paginationControls = document.getElementById('paginationControls');
    
    if (paginationState.totalPages <= 1) {
        paginationContainer.classList.add('hidden');
        return;
    }
    
    paginationContainer.classList.remove('hidden');
    
    const startItem = ((paginationState.currentPage - 1) * paginationState.pageSize) + 1;
    const endItem = Math.min(paginationState.currentPage * paginationState.pageSize, paginationState.totalCount);
    paginationInfo.textContent = `Showing ${startItem}-${endItem} of ${paginationState.totalCount} products`;
    
    document.getElementById('pageSizeSelect').value = paginationState.pageSize;
    
    let paginationHTML = '';
    
    // Previous button
    paginationHTML += `
        <button class="pagination-btn" ${!paginationState.hasPrevious ? 'disabled' : ''} 
                onclick="goToPage(${paginationState.currentPage - 1})">
            <i class="fas fa-chevron-left"></i> Previous
        </button>
    `;
    
    // Page numbers
    const maxVisiblePages = 5;
    let startPage = Math.max(1, paginationState.currentPage - Math.floor(maxVisiblePages / 2));
    let endPage = Math.min(paginationState.totalPages, startPage + maxVisiblePages - 1);
    
    if (endPage - startPage + 1 < maxVisiblePages) {
        startPage = Math.max(1, endPage - maxVisiblePages + 1);
    }
    
    if (startPage > 1) {
        paginationHTML += `
            <button class="pagination-btn" onclick="goToPage(1)">1</button>
        `;
        if (startPage > 2) {
            paginationHTML += `<span class="pagination-btn" style="border: none; cursor: default;">...</span>`;
        }
    }
    
    for (let i = startPage; i <= endPage; i++) {
        paginationHTML += `
            <button class="pagination-btn ${i === paginationState.currentPage ? 'active' : ''}" 
                    onclick="goToPage(${i})">
                ${i}
            </button>
        `;
    }
    
    if (endPage < paginationState.totalPages) {
        if (endPage < paginationState.totalPages - 1) {
            paginationHTML += `<span class="pagination-btn" style="border: none; cursor: default;">...</span>`;
        }
        paginationHTML += `
            <button class="pagination-btn" onclick="goToPage(${paginationState.totalPages})">
                ${paginationState.totalPages}
            </button>
        `;
    }
    
    // Next button
    paginationHTML += `
        <button class="pagination-btn" ${!paginationState.hasNext ? 'disabled' : ''} 
                onclick="goToPage(${paginationState.currentPage + 1})">
            Next <i class="fas fa-chevron-right"></i>
        </button>
    `;
    
    paginationControls.innerHTML = paginationHTML;
}

// Main product loading function
async function loadProducts() {
    await loadCategoriesForFilter();
    await loadProductsWithFilters();
}

async function loadProductsWithFilters() {
    const loadingElement = document.getElementById('productsLoading');
    const gridElement = document.getElementById('productsGrid');
    const resultsInfo = document.getElementById('resultsInfo');
    
    loadingElement.classList.remove('hidden');
    gridElement.innerHTML = '';
    resultsInfo.classList.add('hidden');

    try {
        const params = new URLSearchParams();
        
        if (currentFilters.search) params.append('q', currentFilters.search);
        if (currentFilters.category) params.append('category', currentFilters.category);
        if (currentFilters.minPrice) params.append('min_price', currentFilters.minPrice);
        if (currentFilters.maxPrice) params.append('max_price', currentFilters.maxPrice);
        if (currentFilters.sort) params.append('sort', currentFilters.sort);
        
        const page = Math.max(1, parseInt(paginationState.currentPage) || 1);
        const pageSize = Math.max(1, parseInt(paginationState.pageSize) || 15);
        
        params.append('page', page);
        params.append('page_size', pageSize);

        const url = `${PRODUCTS_API}/?${params.toString()}`;
        console.log('📡 API Request:', url);
        
        const response = await fetch(url);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📦 API Response:', data);
            
            if (data.results !== undefined) {
                products = data.results || [];
                paginationState = {
                    currentPage: data.current_page || 1,
                    pageSize: data.page_size || pageSize,
                    totalPages: data.total_pages || 1,
                    totalCount: data.total_count || products.length,
                    hasNext: data.has_next || false,
                    hasPrevious: data.has_previous || false
                };
            } else if (Array.isArray(data)) {
                products = data;
                paginationState = {
                    currentPage: 1,
                    pageSize: products.length,
                    totalPages: 1,
                    totalCount: products.length,
                    hasNext: false,
                    hasPrevious: false
                };
            } else {
                console.error('❌ Unexpected API response format:', data);
                products = [];
                paginationState = {
                    currentPage: 1,
                    pageSize: pageSize,
                    totalPages: 1,
                    totalCount: 0,
                    hasNext: false,
                    hasPrevious: false
                };
            }
            
            // Display results info
            if (Object.keys(currentFilters).some(key => currentFilters[key])) {
                let filterText = [];
                if (currentFilters.search) filterText.push(`Search: "${currentFilters.search}"`);
                if (currentFilters.category) {
                    const categorySelect = document.getElementById('categoryFilter');
                    const categoryName = categorySelect ? 
                        categorySelect.options[categorySelect.selectedIndex]?.text : 
                        currentFilters.category;
                    filterText.push(`Category: ${categoryName}`);
                }
                if (currentFilters.minPrice || currentFilters.maxPrice) {
                    const priceRange = [];
                    if (currentFilters.minPrice) priceRange.push(`From $${currentFilters.minPrice}`);
                    if (currentFilters.maxPrice) priceRange.push(`To $${currentFilters.maxPrice}`);
                    filterText.push(`Price: ${priceRange.join(' ')}`);
                }
                if (currentFilters.sort) {
                    const sortSelect = document.getElementById('sortOption');
                    const sortText = sortSelect ? 
                        sortSelect.options[sortSelect.selectedIndex]?.text : 
                        currentFilters.sort;
                    filterText.push(`Sorted by: ${sortText}`);
                }
                
                resultsInfo.innerHTML = `
                    <strong>${paginationState.totalCount} products found</strong>
                    ${filterText.length ? `<br><small>${filterText.join(' • ')}</small>` : ''}
                `;
                resultsInfo.classList.remove('hidden');
            }
            
            displayProducts(products);
            renderPaginationControls();
        } else {
            const errorText = await response.text();
            console.error('❌ API Error Response:', errorText);
            throw new Error(`HTTP ${response.status}: ${errorText}`);
        }
    } catch (error) {
        console.error('❌ Error loading products:', error);
        gridElement.innerHTML = `
            <div class="error w-full text-center">
                <h3>❌ Error loading products</h3>
                <p>${error.message}</p>
                <button class="btn-secondary mt-2" onclick="loadProducts()">Try Again</button>
            </div>
        `;
        document.getElementById('paginationContainer').classList.add('hidden');
    } finally {
        loadingElement.classList.add('hidden');
    }
}