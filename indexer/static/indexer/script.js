// Простая анимация плавного появления карточек
document.addEventListener("DOMContentLoaded", () => {
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
// --- ЛОГИКА ТЕМНОЙ ТЕМЫ ---
document.addEventListener("DOMContentLoaded", () => {
    const themeToggleBtn = document.getElementById("theme-toggle");
    const body = document.documentElement; // Берем тег <html>

    // 1. Проверяем, есть ли уже сохраненная тема в памяти браузера
    const savedTheme = localStorage.getItem("theme");
    
    // Если сохранена темная, сразу включаем её
    if (savedTheme === "dark") {
        body.setAttribute("data-theme", "dark");
        themeToggleBtn.textContent = "☀️"; // Меняем иконку на солнце
    }

    // 2. Обрабатываем клик по кнопке
    themeToggleBtn.addEventListener("click", () => {
        // Проверяем текущую тему
        if (body.getAttribute("data-theme") === "dark") {
            // Переключаем на светлую
            body.removeAttribute("data-theme");
            localStorage.setItem("theme", "light");
            themeToggleBtn.textContent = "🌙";
        } else {
            // Переключаем на темную
            body.setAttribute("data-theme", "dark");
            localStorage.setItem("theme", "dark");
            themeToggleBtn.textContent = "☀️";
        }
    });
});
document.addEventListener("DOMContentLoaded", () => {
    // ... твой старый код для темы и анимации карточек ...

    // Логика Сайдбара
    const menuBtn = document.getElementById('menu-btn');
    const closeBtn = document.getElementById('close-btn');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('overlay');

    function toggleSidebar() {
        sidebar.classList.toggle('active');
        overlay.classList.toggle('active');
    }

    menuBtn.addEventListener('click', toggleSidebar);
    closeBtn.addEventListener('click', toggleSidebar);
    overlay.addEventListener('click', toggleSidebar); // Закрываем при клике на темный фон
});