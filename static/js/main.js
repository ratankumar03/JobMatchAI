// JobMatchAI - Main JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const mobileMenuToggle = document.querySelector('.mobile-menu-toggle');
    const navMenu = document.querySelector('.nav-menu');

    if (mobileMenuToggle && navMenu) {
        // Toggle menu on click
        mobileMenuToggle.addEventListener('click', function() {
            navMenu.classList.toggle('active');

            // Animate hamburger icon
            const icon = this.querySelector('i');
            if (icon) {
                if (navMenu.classList.contains('active')) {
                    icon.classList.remove('fa-bars');
                    icon.classList.add('fa-times');
                } else {
                    icon.classList.remove('fa-times');
                    icon.classList.add('fa-bars');
                }
            }
        });

        // Close menu when clicking a link
        const navLinks = navMenu.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                if (window.innerWidth <= 768) {
                    navMenu.classList.remove('active');
                    const icon = mobileMenuToggle.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            });
        });

        // Close menu when clicking outside
        document.addEventListener('click', function(event) {
            if (window.innerWidth <= 768) {
                const isClickInsideMenu = navMenu.contains(event.target);
                const isClickOnToggle = mobileMenuToggle.contains(event.target);

                if (!isClickInsideMenu && !isClickOnToggle && navMenu.classList.contains('active')) {
                    navMenu.classList.remove('active');
                    const icon = mobileMenuToggle.querySelector('i');
                    if (icon) {
                        icon.classList.remove('fa-times');
                        icon.classList.add('fa-bars');
                    }
                }
            }
        });
    }

    const themeToggle = document.getElementById('themeToggle');
    const savedTheme = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;

    function setTheme(theme) {
        if (theme === 'dark') {
            document.documentElement.setAttribute('data-theme', 'dark');
            localStorage.setItem('theme', 'dark');
        } else {
            document.documentElement.removeAttribute('data-theme');
            localStorage.setItem('theme', 'light');
        }
    }

    if (savedTheme) {
        setTheme(savedTheme);
    } else if (prefersDark) {
        setTheme('dark');
    }

    if (themeToggle) {
        themeToggle.addEventListener('click', () => {
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            setTheme(isDark ? 'light' : 'dark');
        });
    }
    
    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Add animation on scroll
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);
    
    document.querySelectorAll('.feature-card, .job-card, .info-card').forEach(el => {
        observer.observe(el);
    });

    const featureCards = Array.from(document.querySelectorAll('.feature-card'));
    const featureCycleClasses = [
        'color-cycle-1',
        'color-cycle-2',
        'color-cycle-3',
        'color-cycle-4',
        'color-cycle-5'
    ];

    function advanceFeatureColor(card) {
        const currentIndex = Number(card.dataset.colorIndex || '-1');
        const nextIndex = (currentIndex + 1) % featureCycleClasses.length;

        featureCycleClasses.forEach(cls => card.classList.remove(cls));
        card.classList.add(featureCycleClasses[nextIndex]);
        card.dataset.colorIndex = String(nextIndex);
    }

    if (featureCards.length) {
        featureCards.forEach(card => {
            card.setAttribute('tabindex', '0');
            advanceFeatureColor(card);
            card.addEventListener('click', () => {
                advanceFeatureColor(card);
            });
            card.addEventListener('keydown', (event) => {
                if (event.key === 'Enter' || event.key === ' ') {
                    event.preventDefault();
                    card.click();
                }
            });
        });

        setInterval(() => {
            featureCards.forEach(card => {
                advanceFeatureColor(card);
            });
        }, 10000);
    }

    const uploadCycleTargets = Array.from(
        document.querySelectorAll('.upload-section .upload-instructions li, .upload-section .info-card')
    );
    const cycleClasses = [
        'color-cycle-1',
        'color-cycle-2',
        'color-cycle-3',
        'color-cycle-4',
        'color-cycle-5'
    ];

    if (uploadCycleTargets.length) {
        uploadCycleTargets.forEach(target => {
            target.dataset.colorIndex = '-1';
            target.addEventListener('click', () => {
                const currentIndex = Number(target.dataset.colorIndex);
                const nextIndex = (currentIndex + 1) % cycleClasses.length;

                cycleClasses.forEach(cls => target.classList.remove(cls));
                target.classList.add(cycleClasses[nextIndex]);
                target.dataset.colorIndex = String(nextIndex);
            });
        });
    }

    const chatCycleTargets = Array.from(
        document.querySelectorAll('.chatbot-section .chat-info-card, .chatbot-section .suggestion-chip')
    );
    const chatCycleClasses = [
        'chat-color-cycle-1',
        'chat-color-cycle-2',
        'chat-color-cycle-3',
        'chat-color-cycle-4',
        'chat-color-cycle-5'
    ];

    function advanceChatColor(target) {
        const currentIndex = Number(target.dataset.colorIndex || '-1');
        const nextIndex = (currentIndex + 1) % chatCycleClasses.length;

        chatCycleClasses.forEach(cls => target.classList.remove(cls));
        target.classList.add(chatCycleClasses[nextIndex]);
        target.dataset.colorIndex = String(nextIndex);
    }

    if (chatCycleTargets.length) {
        chatCycleTargets.forEach(target => {
            advanceChatColor(target);
            target.addEventListener('click', () => {
                advanceChatColor(target);
            });
        });

        setInterval(() => {
            chatCycleTargets.forEach(target => {
                advanceChatColor(target);
            });
        }, 5000);
    }
});

// Utility function to show notifications
function showNotification(message, type = 'info') {
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.textContent = message;
    
    document.body.appendChild(notification);
    
    setTimeout(() => {
        notification.classList.add('show');
    }, 100);
    
    setTimeout(() => {
        notification.classList.remove('show');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Copy to clipboard function
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showNotification('Link copied to clipboard!', 'success');
        }).catch(() => {
            showNotification('Failed to copy link', 'error');
        });
    }
}
