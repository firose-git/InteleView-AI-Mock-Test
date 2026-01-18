// Dashboard JavaScript - Professional TCS NQT Style

document.addEventListener('DOMContentLoaded', function() {
    // Initialize dashboard
    initializeDashboard();
    
    // Set up event listeners
    setupEventListeners();
    
    // Start real-time updates
    startRealTimeUpdates();
    
    // Initialize animations
    initializeAnimations();
});

// Dashboard Initialization
function initializeDashboard() {
    // Update current time and date
    updateDateTime();
    
    // Set active menu item
    setActiveMenuItem();
    
    // Initialize tooltips
    initializeTooltips();
    
    // Load user preferences
    loadUserPreferences();
    
    // Initialize progress bars
    initializeProgressBars();
    
    // Add fade-in animation to content
    document.querySelector('.content-area').classList.add('fade-in');
}

// Event Listeners Setup
function setupEventListeners() {
    // Mobile menu toggle
    const mobileMenuToggle = document.getElementById('mobileMenuToggle');
    const sidebarToggle = document.getElementById('sidebarToggle');
    const overlay = document.getElementById('overlay');
    const sidebar = document.getElementById('sidebar');
    
    if (mobileMenuToggle) {
        mobileMenuToggle.addEventListener('click', toggleSidebar);
    }
    
    if (sidebarToggle) {
        sidebarToggle.addEventListener('click', toggleSidebar);
    }
    
    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }
    
    // Menu item clicks
    document.querySelectorAll('.menu-link').forEach(link => {
        link.addEventListener('click', function(e) {
            // Show loading spinner
            showLoadingSpinner();
            
            // Add active class
            document.querySelectorAll('.menu-link').forEach(l => l.classList.remove('active'));
            this.classList.add('active');
            
            // Store active menu
            localStorage.setItem('activeMenu', this.dataset.page);
            
            // Simulate loading delay
            setTimeout(() => {
                hideLoadingSpinner();
            }, 1000);
        });
    });
    
    // Dashboard list items
    document.querySelectorAll('.dashboard-list a').forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add ripple effect
            addRippleEffect(this, e);
            
            // Show loading spinner
            showLoadingSpinner();
            
            // Simulate navigation
            setTimeout(() => {
                hideLoadingSpinner();
                // Here you would normally navigate to the page
                console.log('Navigating to:', this.href);
            }, 1500);
        });
    });
    
    // Action buttons
    document.querySelectorAll('.action-btn').forEach(btn => {
        btn.addEventListener('click', function(e) {
            e.preventDefault();
            
            // Add click animation
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-2px)';
            }, 150);
            
            // Show success message
            showNotification('Action completed successfully!', 'success');
        });
    });
    
    // Feature cards hover effects
    document.querySelectorAll('.feature-card').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
    });
    
    // Keyboard shortcuts
    document.addEventListener('keydown', function(e) {
        // Alt + M for mobile menu
        if (e.altKey && e.key === 'm') {
            e.preventDefault();
            toggleSidebar();
        }
        
        // Alt + 1-3 for quick navigation
        if (e.altKey && ['1', '2', '3'].includes(e.key)) {
            e.preventDefault();
            const menuItems = document.querySelectorAll('.menu-link');
            const index = parseInt(e.key) - 1;
            if (menuItems[index]) {
                menuItems[index].click();
            }
        }
    });
}

// Sidebar Toggle Functions
function toggleSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.toggle('show');
        overlay.classList.toggle('show');
        
        // Update mobile menu toggle icon
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        if (mobileMenuToggle) {
            const icon = mobileMenuToggle.querySelector('i');
            if (sidebar.classList.contains('show')) {
                icon.className = 'fas fa-times';
            } else {
                icon.className = 'fas fa-bars';
            }
        }
    }
}

function closeSidebar() {
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');
    
    if (sidebar && overlay) {
        sidebar.classList.remove('show');
        overlay.classList.remove('show');
        
        // Reset mobile menu toggle icon
        const mobileMenuToggle = document.getElementById('mobileMenuToggle');
        if (mobileMenuToggle) {
            const icon = mobileMenuToggle.querySelector('i');
            icon.className = 'fas fa-bars';
        }
    }
}

// Date and Time Updates
function updateDateTime() {
    const now = new Date();
    
    // Update time
    const timeElement = document.getElementById('currentTime');
    if (timeElement) {
        timeElement.textContent = now.toLocaleTimeString('en-US', {
            hour: '2-digit',
            minute: '2-digit',
            second: '2-digit'
        });
    }
    
    // Update date
    const dateElement = document.getElementById('currentDate');
    if (dateElement) {
        dateElement.textContent = now.toLocaleDateString('en-US', {
            weekday: 'long',
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });
    }
}

// Set Active Menu Item
function setActiveMenuItem() {
    const activeMenu = localStorage.getItem('activeMenu') || 'dashboard';
    const menuLink = document.querySelector(`[data-page="${activeMenu}"]`);
    
    if (menuLink) {
        document.querySelectorAll('.menu-link').forEach(link => {
            link.classList.remove('active');
        });
        menuLink.classList.add('active');
    }
}

// Initialize Tooltips
function initializeTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', function() {
            const tooltipText = this.getAttribute('data-tooltip');
            const tooltip = document.createElement('div');
            tooltip.className = 'tooltip';
            tooltip.textContent = tooltipText;
            document.body.appendChild(tooltip);
            
            const rect = this.getBoundingClientRect();
            tooltip.style.left = rect.left + rect.width / 2 - tooltip.offsetWidth / 2 + 'px';
            tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
            
            setTimeout(() => {
                tooltip.classList.add('show');
            }, 10);
        });
        
        element.addEventListener('mouseleave', function() {
            const tooltip = document.querySelector('.tooltip');
            if (tooltip) {
                tooltip.remove();
            }
        });
    });
}

// Load User Preferences
function loadUserPreferences() {
    const theme = localStorage.getItem('theme') || 'light';
    const language = localStorage.getItem('language') || 'en';
    
    // Apply theme
    document.body.setAttribute('data-theme', theme);
    
    // Apply language
    document.documentElement.setAttribute('lang', language);
    
    // Update theme toggle button
    const themeToggle = document.getElementById('themeToggle');
    if (themeToggle) {
        themeToggle.checked = theme === 'dark';
        themeToggle.addEventListener('change', function() {
            const newTheme = this.checked ? 'dark' : 'light';
            document.body.setAttribute('data-theme', newTheme);
            localStorage.setItem('theme', newTheme);
        });
    }
}

// Initialize Progress Bars
function initializeProgressBars() {
    const progressBars = document.querySelectorAll('.progress-bar');
    
    progressBars.forEach(bar => {
        const progress = bar.getAttribute('data-progress') || '0';
        const progressFill = bar.querySelector('.progress-fill');
        
        if (progressFill) {
            setTimeout(() => {
                progressFill.style.width = progress + '%';
            }, 500);
        }
    });
}

// Real-time Updates
function startRealTimeUpdates() {
    // Update time every second
    setInterval(updateDateTime, 1000);
    
    // Update notifications every 30 seconds
    setInterval(updateNotifications, 30000);
    
    // Update stats every 5 minutes
    setInterval(updateStats, 300000);
}

// Update Notifications
function updateNotifications() {
    const notificationCount = document.getElementById('notificationCount');
    if (notificationCount) {
        // Simulate new notification
        const currentCount = parseInt(notificationCount.textContent) || 0;
        if (Math.random() < 0.3) { // 30% chance of new notification
            notificationCount.textContent = currentCount + 1;
            notificationCount.style.display = 'block';
            
            // Show notification popup
            showNotification('You have a new notification!', 'info');
        }
    }
}

// Update Stats
function updateStats() {
    const statElements = document.querySelectorAll('.stat-value');
    
    statElements.forEach(element => {
        const currentValue = parseInt(element.textContent) || 0;
        const change = Math.floor(Math.random() * 10) - 5; // Random change between -5 and +5
        const newValue = Math.max(0, currentValue + change);
        
        animateValue(element, currentValue, newValue, 1000);
    });
}

// Animate Value
function animateValue(element, start, end, duration) {
    const startTime = performance.now();
    
    function updateValue(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        const currentValue = Math.floor(start + (end - start) * progress);
        element.textContent = currentValue;
        
        if (progress < 1) {
            requestAnimationFrame(updateValue);
        }
    }
    
    requestAnimationFrame(updateValue);
}

// Loading Spinner
function showLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.display = 'flex';
        spinner.style.opacity = '1';
    }
}

function hideLoadingSpinner() {
    const spinner = document.getElementById('loadingSpinner');
    if (spinner) {
        spinner.style.opacity = '0';
        setTimeout(() => {
            spinner.style.display = 'none';
        }, 300);
    }
}

// Notification System
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <i class="fas fa-${getNotificationIcon(type)}"></i>
            <span>${message}</span>
        </div>
        <button class="notification-close" onclick="this.parentElement.remove()">
            <i class="fas fa-times"></i>
        </button>
    `;
    
    document.body.appendChild(notification);
    
    // Show notification
    setTimeout(() => {
        notification.classList.add('show');
    }, 10);
    
    // Auto remove after 5 seconds
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            if (notification.parentElement) {
                notification.remove();
            }
        }, 300);
    }, 5000);
}

function getNotificationIcon(type) {
    switch (type) {
        case 'success': return 'check-circle';
        case 'error': return 'exclamation-circle';
        case 'warning': return 'exclamation-triangle';
        case 'info':
        default: return 'info-circle';
    }
}

// Ripple Effect
function addRippleEffect(element, event) {
    const ripple = document.createElement('span');
    ripple.className = 'ripple';
    
    const rect = element.getBoundingClientRect();
    const size = Math.max(rect.width, rect.height);
    const x = event.clientX - rect.left - size / 2;
    const y = event.clientY - rect.top - size / 2;
    
    ripple.style.width = ripple.style.height = size + 'px';
    ripple.style.left = x + 'px';
    ripple.style.top = y + 'px';
    
    element.appendChild(ripple);
    
    setTimeout(() => {
        ripple.remove();
    }, 600);
}

// Initialize Animations
function initializeAnimations() {
    // Fade in animation for cards
    const cards = document.querySelectorAll('.card, .feature-card');
    cards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            card.style.transition = 'opacity 0.6s ease, transform 0.6s ease';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 100);
    });
    
    // Parallax effect for hero section
    window.addEventListener('scroll', () => {
        const scrolled = window.pageYOffset;
        const hero = document.querySelector('.hero-section');
        
        if (hero) {
            hero.style.transform = `translateY(${scrolled * 0.5}px)`;
        }
    });
}

// Search Functionality
function initializeSearch() {
    const searchInput = document.getElementById('searchInput');
    const searchResults = document.getElementById('searchResults');
    
    if (searchInput) {
        searchInput.addEventListener('input', function() {
            const query = this.value.toLowerCase();
            
            if (query.length > 2) {
                performSearch(query);
            } else {
                hideSearchResults();
            }
        });
        
        // Hide results when clicking outside
        document.addEventListener('click', function(e) {
            if (!searchInput.contains(e.target) && !searchResults.contains(e.target)) {
                hideSearchResults();
            }
        });
    }
}

function performSearch(query) {
    // Mock search data
    const searchData = [
        { title: 'Dashboard', url: '/dashboard', type: 'page' },
        { title: 'Profile Settings', url: '/profile', type: 'page' },
        { title: 'Practice Tests', url: '/practice', type: 'feature' },
        { title: 'Mock Interview', url: '/interview', type: 'feature' },
        { title: 'Study Material', url: '/study', type: 'resource' }
    ];
    
    const results = searchData.filter(item => 
        item.title.toLowerCase().includes(query)
    );
    
    displaySearchResults(results);
}

function displaySearchResults(results) {
    const searchResults = document.getElementById('searchResults');
    
    if (searchResults) {
        searchResults.innerHTML = '';
        
        results.forEach(result => {
            const resultItem = document.createElement('div');
            resultItem.className = 'search-result-item';
            resultItem.innerHTML = `
                <i class="fas fa-${getResultIcon(result.type)}"></i>
                <div>
                    <div class="result-title">${result.title}</div>
                    <div class="result-type">${result.type}</div>
                </div>
            `;
            
            resultItem.addEventListener('click', () => {
                console.log('Navigate to:', result.url);
                hideSearchResults();
            });
            
            searchResults.appendChild(resultItem);
        });
        
        searchResults.style.display = 'block';
    }
}

function getResultIcon(type) {
    switch (type) {
        case 'page': return 'file-alt';
        case 'feature': return 'cog';
        case 'resource': return 'book';
        default: return 'search';
    }
}

function hideSearchResults() {
    const searchResults = document.getElementById('searchResults');
    if (searchResults) {
        searchResults.style.display = 'none';
    }
}

// Performance Monitoring
function initializePerformanceMonitoring() {
    // Monitor page load time
    window.addEventListener('load', function() {
        const loadTime = performance.now();
        console.log(`Page loaded in ${loadTime.toFixed(2)}ms`);
        
        // Log to analytics (in real app)
        if (typeof gtag !== 'undefined') {
            gtag('event', 'page_load_time', {
                value: Math.round(loadTime)
            });
        }
    });
    
    // Monitor user interactions
    document.addEventListener('click', function(e) {
        if (e.target.matches('[data-track]')) {
            const action = e.target.getAttribute('data-track');
            console.log(`User action: ${action}`);
            
            // Log to analytics (in real app)
            if (typeof gtag !== 'undefined') {
                gtag('event', 'user_interaction', {
                    action: action
                });
            }
        }
    });
}

// Initialize all components
document.addEventListener('DOMContentLoaded', function() {
    initializeSearch();
    initializePerformanceMonitoring();
});

// Utility Functions
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Export functions for testing
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeDashboard,
        toggleSidebar,
        showNotification,
        updateDateTime
    };
}