// Dashboard interaktiv funksiyalari

document.addEventListener('DOMContentLoaded', function() {
    // Sidebar menyusi faollashtirish
    const menuItems = document.querySelectorAll('.menu-item');

    menuItems.forEach(item => {
        item.addEventListener('click', function(e) {
            e.preventDefault();

            // Barcha menyu elementlaridan active klassini olib tashlash
            menuItems.forEach(i => i.classList.remove('active'));

            // Bosilgan elementga active klassini qo'shish
            this.classList.add('active');

            // Bu yerda haqiqiy sahifaga o'tish amalga oshirilishi kerak
            console.log(`Sahifaga o'tildi: ${this.querySelector('span').textContent}`);
        });
    });

    // Statistik kartalarga hover effekt
    const statCards = document.querySelectorAll('.stat-card');

    statCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            const icon = this.querySelector('.stat-icon');
            icon.style.transform = 'scale(1.1)';
        });

        card.addEventListener('mouseleave', function() {
            const icon = this.querySelector('.stat-icon');
            icon.style.transform = 'scale(1)';
        });
    });

    // Chart bar larga hover effekt
    const bars = document.querySelectorAll('.bar');

    bars.forEach(bar => {
        bar.addEventListener('mouseenter', function() {
            this.style.transform = 'scale(1.05)';
            const day = this.querySelector('span').textContent;
            console.log(`${day} kuni faollik: ${this.style.height}`);
        });

        bar.addEventListener('mouseleave', function() {
            this.style.transform = 'scale(1)';
        });
    });

    // User profile menu (keyinchalik to'ldirilishi mumkin)
    const userProfile = document.querySelector('.user-profile');

    userProfile.addEventListener('click', function() {
        console.log('User profile menusi ochildi');
        // Bu yerda dropdown menyuni ochish amalga oshirilishi kerak
    });

    // Ma'lumotlar yangilanishini simulyatsiya qilish
    function updateStats() {
        // Bu funksiya backend API orqali real ma'lumotlarni oladi
        // Hozircha simulyatsiya qilamiz
        const counts = document.querySelectorAll('.count');

        // Har 10 soniyada raqamlar biroz o'zgaradi (simulyatsiya uchun)
        setInterval(() => {
            counts.forEach(count => {
                const currentValue = parseInt(count.textContent);
                if (!isNaN(currentValue)) {
                    // 1-5 orasida tasodifiy o'zgarish
                    const change = Math.floor(Math.random() * 5) - 2; // -2 dan +2 gacha
                    const newValue = Math.max(1, currentValue + change); // 1 dan pastga tushmasin
                    count.textContent = newValue;
                }
            });
        }, 10000);
    }

    updateStats();

    // So'nggi faollik vaqtini real vaqtga moslash
    const activityTimes = document.querySelectorAll('.activity-time');
    const now = new Date();

    // Har bir faollik uchun dinamik vaqt (simulyatsiya)
    activityTimes.forEach((timeElement, index) => {
        const timeText = timeElement.textContent;

        // Agar vaqt "daqiqa oldin", "soat oldin" formatida bo'lsa
        if (timeText.includes('daqiqa oldin') || timeText.includes('soat oldin')) {
            // Bu yerda haqiqiy vaqtni hisoblash logikasi bo'lishi kerak
            // Hozircha faqat matnni saqlaymiz
        }
    });

    // Dashboardga xush kelibsiz xabari
    console.log('AJOU Admin Dashboard yuklandi. Xush kelibsiz!');
});