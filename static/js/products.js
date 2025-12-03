
console.log('📦 products.js loaded - PRODUCTS_API:', PRODUCTS_API);

// Global variables (if not defined in utils.js)
if (typeof window.products === 'undefined') window.products = [];
if (typeof window.categories === 'undefined') window.categories = [];
if (typeof window.currentFilters === 'undefined') {
    window.currentFilters = {
        search: '',
        category: '',
        minPrice: '',
        maxPrice: '',
        sort: ''
    };
}
if (typeof window.paginationState === 'undefined') {
    window.paginationState = {
        currentPage: 1,
        pageSize: 15,
        totalPages: 1,
        totalCount: 0,
        hasNext: false,
        hasPrevious: false
    };
}

// Product Functions
async function loadFeaturedProducts() {
    console.log('⭐ Loading featured products...');
    try {
        // Try different endpoint formats
        const urls = [
            `${PRODUCTS_API}/?is_featured=true&page_size=4`,
            `${PRODUCTS_API}/?featured=true&page_size=4`,
            `${PRODUCTS_API}/?is_featured=true`
        ];
        
        let featuredProducts = [];
        
        for (let url of urls) {
            try {
                console.log('Trying URL:', url);
                const response = await fetch(url);
                if (response.ok) {
                    const data = await response.json();
                    featuredProducts = data.results || data;
                    if (featuredProducts.length > 0) {
                        console.log(`✅ Found ${featuredProducts.length} featured products`);
                        break;
                    }
                }
            } catch (error) {
                console.log(`❌ Failed with ${url}:`, error.message);
            }
        }
        
        displayFeaturedProducts(featuredProducts);
    } catch (error) {
        console.error('Error loading featured products:', error);
    }
}

function displayFeaturedProducts(products) {
    const featuredContainer = document.getElementById('featuredProducts');
    if (!featuredContainer) {
        console.warn('❌ featuredProducts element not found');
        return;
    }
    
    if (!products || products.length === 0) {
        featuredContainer.innerHTML = '<div class="info">No featured products available</div>';
        return;
    }

    console.log(`🎯 Displaying ${products.length} featured products`);
    featuredContainer.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image-container">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <div class="product-name">${product.name || 'Unnamed Product'}</div>
                <div class="product-price">$${product.price || '0.00'}</div>
                <div class="product-category">
                    <i class="fas fa-tag"></i> ${product.category?.name || product.category_name || 'Uncategorized'}
                </div>
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
    if (!gridElement) {
        console.error('❌ productsGrid element not found');
        return;
    }
    
    if (!products || products.length === 0) {
        gridElement.innerHTML = `
            <div class="info w-full text-center">
                <h3>No products found</h3>
                <p>Try adjusting your search criteria or filters</p>
                <button class="btn-secondary mt-2" onclick="clearFilters()">Clear All Filters</button>
            </div>
        `;
        return;
    }

    console.log(`🛍️ Displaying ${products.length} products`);
    gridElement.innerHTML = products.map(product => `
        <div class="product-card">
            <div class="product-image-container">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <div class="product-name">${product.name || 'Unnamed Product'}</div>
                <div class="product-price">$${product.price || '0.00'}</div>
                <div class="product-category">
                    <i class="fas fa-tag"></i> ${product.category?.name || product.category_name || 'Uncategorized'}
                </div>
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
    console.log(`🔍 Loading product detail for ID: ${productId}`);
    try {
        const response = await fetch(`${PRODUCTS_API}/${productId}/`);
        if (response.ok) {
            const product = await response.json();
            displayProductDetail(product);
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('Error loading product details:', error);
        const detailElement = document.getElementById('productDetail');
        if (detailElement) {
            detailElement.innerHTML = `<div class="error">❌ Error loading product details: ${error.message}</div>`;
        }
    }
}

function displayProductDetail(product) {
    const detailElement = document.getElementById('productDetail');
    if (!detailElement) return;
    
    detailElement.innerHTML = `
        <div class="product-card">
            <div class="product-image-container" style="height: 400px;">
                ${product.image ? 
                    `<img src="${product.image}" alt="${product.name}" class="product-image">` : 
                    `<div class="product-image-placeholder">📦</div>`
                }
            </div>
            <div class="product-info">
                <h2>${product.name || 'Unnamed Product'}</h2>
                <div class="product-price">$${product.price || '0.00'}</div>
                <p><strong><i class="fas fa-tag"></i> Category:</strong> ${product.category?.name || 'Uncategorized'}</p>
                <p><strong><i class="fas fa-align-left"></i> Description:</strong> ${product.description || 'No description available'}</p>
                <p><strong><i class="fas fa-box"></i> Stock:</strong> ${product.stock_quantity || 0} available</p>
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
    console.log('📂 Loading categories...');
    const loadingElement = document.getElementById('categoriesLoading');
    const listElement = document.getElementById('categoriesList');
    
    if (!loadingElement || !listElement) {
        console.error('❌ Category elements not found');
        return;
    }
    
    loadingElement.classList.remove('hidden');
    listElement.innerHTML = '';

    try {
        const response = await fetch(`${CATEGORIES_API}/`);
        if (response.ok) {
            const data = await response.json();
            
            if (Array.isArray(data)) {
                categories = data;
            } else if (data.results && Array.isArray(data.results)) {
                categories = data.results;
            } else {
                console.error('Unexpected categories format:', data);
                categories = [];
            }
            
            console.log(`✅ Loaded ${categories.length} categories`);
            displayCategories(categories);
        } else {
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('Categories error:', error);
        listElement.innerHTML = `<div class="error">❌ Error loading categories: ${error.message}</div>`;
    } finally {
        loadingElement.classList.add('hidden');
    }
}

function displayCategories(categories) {
    const listElement = document.getElementById('categoriesList');
    if (!listElement) return;
    
    if (!categories || categories.length === 0) {
        listElement.innerHTML = '<div class="info">No categories found</div>';
        return;
    }

    listElement.innerHTML = categories.map(category => `
        <div class="product-card" style="cursor: pointer;" onclick="filterProductsByCategory(${category.id}, '${category.name}')">
            <div class="product-info">
                <h3><i class="fas fa-tags"></i> ${category.name || 'Unnamed Category'}</h3>
                <p class="product-category">${category.description || 'No description available'}</p>
                <button class="btn-secondary" onclick="event.stopPropagation(); filterProductsByCategory(${category.id}, '${category.name}')">
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
    const searchInput = document.getElementById('globalSearch');
    if (!searchInput) return;
    
    const searchQuery = searchInput.value.trim();
    if (searchQuery) {
        currentFilters.search = searchQuery;
        navigateTo('/products');
        setTimeout(() => {
            const productSearchInput = document.getElementById('searchInput');
            if (productSearchInput) {
                productSearchInput.value = searchQuery;
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
            const data = await response.json();
            
            let categories = [];
            if (Array.isArray(data)) {
                categories = data;
            } else if (data.results && Array.isArray(data.results)) {
                categories = data.results;
            } else if (data.categories && Array.isArray(data.categories)) {
                categories = data.categories;
            } else {
                console.error('Unexpected categories format:', data);
                categories = [];
            }
            
            const categorySelect = document.getElementById('categoryFilter');
            if (categorySelect) {
                categorySelect.innerHTML = '<option value="">All Categories</option>' +
                    categories.map(cat => `<option value="${cat.id}">${cat.name}</option>`).join('');
                
                if (currentFilters.category) {
                    categorySelect.value = currentFilters.category;
                }
            }
        }
    } catch (error) {
        console.error('Error loading categories for filter:', error);
    }
}

function applyFilters() {
    console.log('🔍 Applying filters:', currentFilters);
    currentFilters = {
        search: document.getElementById('searchInput')?.value || '',
        category: document.getElementById('categoryFilter')?.value || '',
        minPrice: document.getElementById('minPrice')?.value || '',
        maxPrice: document.getElementById('maxPrice')?.value || '',
        sort: document.getElementById('sortOption')?.value || ''
    };
    paginationState.currentPage = 1;
    loadProductsWithFilters();
}

function clearFilters() {
    console.log('🧹 Clearing filters');
    const searchInput = document.getElementById('searchInput');
    const categoryFilter = document.getElementById('categoryFilter');
    const minPrice = document.getElementById('minPrice');
    const maxPrice = document.getElementById('maxPrice');
    const sortOption = document.getElementById('sortOption');
    
    if (searchInput) searchInput.value = '';
    if (categoryFilter) categoryFilter.value = '';
    if (minPrice) minPrice.value = '';
    if (maxPrice) maxPrice.value = '';
    if (sortOption) sortOption.value = '';
    
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
    
    if (!paginationContainer || !paginationInfo || !paginationControls) return;
    
    if (paginationState.totalPages <= 1) {
        paginationContainer.classList.add('hidden');
        return;
    }
    
    paginationContainer.classList.remove('hidden');
    
    const startItem = ((paginationState.currentPage - 1) * paginationState.pageSize) + 1;
    const endItem = Math.min(paginationState.currentPage * paginationState.pageSize, paginationState.totalCount);
    paginationInfo.textContent = `Showing ${startItem}-${endItem} of ${paginationState.totalCount} products`;
    
    const pageSizeSelect = document.getElementById('pageSizeSelect');
    if (pageSizeSelect) {
        pageSizeSelect.value = paginationState.pageSize;
    }
    
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
    console.log('📦 Loading products page...');
    await loadCategoriesForFilter();
    await loadProductsWithFilters();
}

async function loadProductsWithFilters() {
    console.log('🔄 loadProductsWithFilters called');
    const loadingElement = document.getElementById('productsLoading');
    const gridElement = document.getElementById('productsGrid');
    const resultsInfo = document.getElementById('resultsInfo');
    
    if (!loadingElement || !gridElement || !resultsInfo) {
        console.error('❌ Required DOM elements not found');
        console.log('- productsLoading:', !!loadingElement);
        console.log('- productsGrid:', !!gridElement);
        console.log('- resultsInfo:', !!resultsInfo);
        return;
    }
    
    loadingElement.classList.remove('hidden');
    gridElement.innerHTML = '';
    resultsInfo.classList.add('hidden');

    try {
        const params = new URLSearchParams();
        
        // Try different parameter names for compatibility
        if (currentFilters.search) {
            params.append('search', currentFilters.search);  // Try 'search'
            params.append('q', currentFilters.search);       // Try 'q' as alternative
        }
        if (currentFilters.category) params.append('category', currentFilters.category);
        
        // Price parameters
        if (currentFilters.minPrice) {
            params.append('price_min', currentFilters.minPrice);
            params.append('min_price', currentFilters.minPrice);  // Alternative
        }
        if (currentFilters.maxPrice) {
            params.append('price_max', currentFilters.maxPrice);
            params.append('max_price', currentFilters.maxPrice);  // Alternative
        }
        
        // Sorting
        if (currentFilters.sort) {
            if (currentFilters.sort === 'price_asc') {
                params.append('ordering', 'price');
                params.append('sort', 'price');  // Alternative
            } else if (currentFilters.sort === 'price_desc') {
                params.append('ordering', '-price');
                params.append('sort', '-price');  // Alternative
            } else if (currentFilters.sort === 'name_asc') {
                params.append('ordering', 'name');
                params.append('sort', 'name');  // Alternative
            } else if (currentFilters.sort === 'name_desc') {
                params.append('ordering', '-name');
                params.append('sort', '-name');  // Alternative
            }
        }
        
        const page = Math.max(1, parseInt(paginationState.currentPage) || 1);
        const pageSize = Math.max(1, parseInt(paginationState.pageSize) || 15);
        
        params.append('page', page);
        params.append('page_size', pageSize);

        const url = `${PRODUCTS_API}/?${params.toString()}`;
        console.log('📡 API Request URL:', url);
        
        const response = await fetch(url);
        console.log('📡 Response status:', response.status);
        
        if (response.ok) {
            const data = await response.json();
            console.log('📦 API Response data:', data);
            
            // Handle different response formats
            if (data.results !== undefined) {
                products = data.results || [];
                
                // Try to extract pagination info
                paginationState = {
                    currentPage: data.current_page || page,
                    pageSize: data.page_size || pageSize,
                    totalPages: data.total_pages || Math.ceil((data.count || products.length) / pageSize) || 1,
                    totalCount: data.total_count || data.count || products.length,
                    hasNext: data.has_next || !!data.next || false,
                    hasPrevious: data.has_previous || !!data.previous || false
                };
            } else if (Array.isArray(data)) {
                // Simple array response
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
            throw new Error(`HTTP ${response.status}`);
        }
    } catch (error) {
        console.error('❌ Error loading products:', error);
        gridElement.innerHTML = `
            <div class="error w-full text-center">
                <h3>❌ Error loading products</h3>
                <p>${error.message}</p>
                <p>API Base URL: ${API_BASE_URL}</p>
                <button class="btn-secondary mt-2" onclick="loadProducts()">Try Again</button>
            </div>
        `;
        const paginationContainer = document.getElementById('paginationContainer');
        if (paginationContainer) {
            paginationContainer.classList.add('hidden');
        }
    } finally {
        loadingElement.classList.add('hidden');
    }
}

// DIRECT CATEGORY FILTERING 
function filterProductsByCategory(categoryId, categoryName) {
    console.log(`🎯 Direct category filtering: ${categoryName} (ID: ${categoryId})`);
    
    // Navigate to products page
    navigateTo('/products');
    
    // Wait for products page to load, then load products directly
    setTimeout(() => {
        // Set the category filter dropdown value
        const categoryFilter = document.getElementById('categoryFilter');
        if (categoryFilter) {
            categoryFilter.value = categoryId;
        }
        
        const loadingElement = document.getElementById('productsLoading');
        const gridElement = document.getElementById('productsGrid');
        const resultsInfo = document.getElementById('resultsInfo');
        
        if (!loadingElement || !gridElement || !resultsInfo) return;
        
        loadingElement.classList.remove('hidden');
        gridElement.innerHTML = '';
        
        resultsInfo.innerHTML = `Showing products in: <strong>${categoryName}</strong>`;
        resultsInfo.classList.remove('hidden');

        // Try different URL patterns
        const urls = [
            `${PRODUCTS_API}/?category=${categoryId}`,
            `${PRODUCTS_API}/?category_id=${categoryId}`,
            `${PRODUCTS_API}/?categories=${categoryId}`
        ];

        const tryUrl = (index) => {
            if (index >= urls.length) {
                gridElement.innerHTML = `
                    <div class="info w-full text-center">
                        <h3>No products found in this category</h3>
                        <button class="btn-secondary mt-2" onclick="clearFilters()">Show All Products</button>
                    </div>
                `;
                loadingElement.classList.add('hidden');
                return;
            }

            console.log('Trying category URL:', urls[index]);
            fetch(urls[index])
                .then(response => {
                    if (!response.ok) throw new Error(`HTTP ${response.status}`);
                    return response.json();
                })
                .then(data => {
                    let products = [];
                    if (data.results !== undefined) {
                        products = data.results || [];
                    } else if (Array.isArray(data)) {
                        products = data;
                    }
                    
                    if (products.length > 0) {
                        console.log(`✅ Found ${products.length} products with URL: ${urls[index]}`);
                        displayProducts(products);
                        const paginationContainer = document.getElementById('paginationContainer');
                        if (paginationContainer) {
                            paginationContainer.classList.add('hidden');
                        }
                    } else {
                        tryUrl(index + 1);
                    }
                })
                .catch(error => {
                    console.log(`❌ Failed with ${urls[index]}:`, error.message);
                    tryUrl(index + 1);
                })
                .finally(() => {
                    loadingElement.classList.add('hidden');
                });
        };

        tryUrl(0);
    }, 300);
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    console.log('📦 products.js DOM ready');
    const path = window.location.pathname;
    
    if (path === '/' || path === '/index.html') {
        console.log('🏠 Home page - loading featured products');
        if (typeof loadFeaturedProducts === 'function') loadFeaturedProducts();
    } else if (path === '/products' || path.includes('/products.html')) {
        console.log('🛍️ Products page - loading products');
        if (typeof loadProducts === 'function') loadProducts();
    } else if (path.startsWith('/product/')) {
        const productId = path.split('/').pop();
        if (productId && !isNaN(productId)) {
            console.log(`🔍 Product detail page - ID: ${productId}`);
            if (typeof loadProductDetail === 'function') loadProductDetail(parseInt(productId));
        }
    } else if (path === '/categories' || path.includes('/categories.html')) {
        console.log('📂 Categories page');
        if (typeof loadCategories === 'function') loadCategories();
    }
});

// Add global access
window.loadFeaturedProducts = loadFeaturedProducts;
window.loadProducts = loadProducts;
window.loadProductDetail = loadProductDetail;
window.displayProducts = displayProducts;
window.applyFilters = applyFilters;
window.clearFilters = clearFilters;
window.filterProductsByCategory = filterProductsByCategory;
window.goToPage = goToPage;
window.changePageSize = changePageSize;

console.log('✅ products.js functions registered globally');