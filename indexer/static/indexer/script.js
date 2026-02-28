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