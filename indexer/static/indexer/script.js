document.addEventListener("DOMContentLoaded", () => {
    // 1. ЛОГИКА ТЕМНОЙ ТЕМЫ
    const themeToggleBtn = document.getElementById("theme-toggle");
    const body = document.documentElement;
    const savedTheme = localStorage.getItem("theme");
    
    if (savedTheme === "dark") {
        body.setAttribute("data-theme", "dark");
        if (themeToggleBtn) themeToggleBtn.textContent = "☀️";
    }

    if (themeToggleBtn) {
        themeToggleBtn.addEventListener("click", () => {
            if (body.getAttribute("data-theme") === "dark") {
                body.removeAttribute("data-theme");
                localStorage.setItem("theme", "light");
                themeToggleBtn.textContent = "🌙";
            } else {
                body.setAttribute("data-theme", "dark");
                localStorage.setItem("theme", "dark");
                themeToggleBtn.textContent = "☀️";
            }
        });
    }

    // 2. ЛОГИКА САЙДБАРА (КАТЕГОРИИ)
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function toggleSidebar() {
        if (sidebar && overlay) {
            sidebar.classList.toggle('active');
            overlay.classList.toggle('active');
        }
    }

    if (menuBtn) menuBtn.addEventListener('click', toggleSidebar);
    if (closeBtn) closeBtn.addEventListener('click', toggleSidebar);
    if (overlay) overlay.addEventListener('click', toggleSidebar);

    // 3. АНИМАЦИЯ КАРТОЧЕК ПРИ ЗАГРУЗКЕ
    const cards = document.querySelectorAll('.video-card');
    cards.forEach((card, index) => {
        card.style.opacity = 0;
        card.style.transform = "translateY(20px)";
        card.style.transition = "all 0.5s ease";
        setTimeout(() => {
            card.style.opacity = 1;
            card.style.transform = "translateY(0)";
        }, 100 * index);
    });
});