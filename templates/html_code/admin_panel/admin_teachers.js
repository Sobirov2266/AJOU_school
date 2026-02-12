// Teachers Page JavaScript

document.addEventListener('DOMContentLoaded', function() {
    // Namuna o'qituvchilar ma'lumotlari (haqiqiy loyihada bu backenddan keladi)
    let teachers = [
        {
            id: 1,
            firstName: "Ali",
            lastName: "Valiyev",
            phone: "+998 90 123 45 67",
            email: "ali.valiyev@ajou.edu",
            subject: "mathematics",
            status: "active",
            notes: "5 yillik tajriba"
        },
        {
            id: 2,
            firstName: "Zarina",
            lastName: "Qodirova",
            phone: "+998 91 234 56 78",
            email: "zarina.qodirova@ajou.edu",
            subject: "english",
            status: "active",
            notes: "IELTS 8.5"
        },
        {
            id: 3,
            firstName: "Olim",
            lastName: "Toshmatov",
            phone: "+998 93 345 67 89",
            email: "olim.toshmatov@ajou.edu",
            subject: "physics",
            status: "inactive",
            notes: ""
        },
        {
            id: 4,
            firstName: "Dilnoza",
            lastName: "Xolmirzayeva",
            phone: "+998 94 456 78 90",
            email: "dilnoza.x@ajou.edu",
            subject: "biology",
            status: "active",
            notes: "PhD darajasi bor"
        },
        {
            id: 5,
            firstName: "Javohir",
            lastName: "Saidov",
            phone: "+998 95 567 89 01",
            email: "javohir.s@ajou.edu",
            subject: "informatics",
            status: "active",
            notes: ""
        },
        {
            id: 6,
            firstName: "Malika",
            lastName: "Raximova",
            phone: "+998 97 678 90 12",
            email: "malika.r@ajou.edu",
            subject: "chemistry",
            status: "active",
            notes: ""
        },
        {
            id: 7,
            firstName: "Sherzod",
            lastName: "Karimov",
            phone: "+998 98 789 01 23",
            email: "sherzod.k@ajou.edu",
            subject: "history",
            status: "active",
            notes: ""
        },
        {
            id: 8,
            firstName: "Farida",
            lastName: "Nosirova",
            phone: "+998 99 890 12 34",
            email: "farida.n@ajou.edu",
            subject: "uzbek",
            status: "active",
            notes: ""
        }
    ];

    // DOM elementlari
    const teachersTableBody = document.getElementById('teachers-table-body');
    const teacherCount = document.getElementById('teacher-count');
    const searchInput = document.getElementById('search-teacher');
    const filterSubject = document.getElementById('filter-subject');
    const addTeacherBtn = document.getElementById('add-teacher-btn');
    const addTeacherModal = document.getElementById('add-teacher-modal');
    const editTeacherModal = document.getElementById('edit-teacher-modal');
    const closeAddModal = document.getElementById('close-add-modal');
    const closeEditModal = document.getElementById('close-edit-modal');
    const cancelAdd = document.getElementById('cancel-add');
    const cancelEdit = document.getElementById('cancel-edit');
    const addTeacherForm = document.getElementById('add-teacher-form');
    const editTeacherForm = document.getElementById('edit-teacher-form');
    const deleteTeacherBtn = document.getElementById('delete-teacher-btn');

    // Fan nomlari
    const subjectNames = {
        "mathematics": "Matematika",
        "physics": "Fizika",
        "chemistry": "Kimyo",
        "biology": "Biologiya",
        "english": "Ingliz tili",
        "uzbek": "O'zbek tili",
        "history": "Tarix",
        "geography": "Geografiya",
        "informatics": "Informatika",
        "other": "Boshqa"
    };

    // O'qituvchilar ro'yxatini ko'rsatish
    function renderTeachers(teachersList = teachers) {
        teachersTableBody.innerHTML = '';

        teachersList.forEach(teacher => {
            const row = document.createElement('tr');

            row.innerHTML = `
                <td>${teacher.id}</td>
                <td>${teacher.firstName}</td>
                <td>${teacher.lastName}</td>
                <td>${teacher.phone}</td>
                <td>${teacher.email}</td>
                <td>${subjectNames[teacher.subject] || teacher.subject}</td>
                <td>
                    <span class="status-badge status-${teacher.status}">
                        ${teacher.status === 'active' ? 'Faol' : 'Faol emas'}
                    </span>
                </td>
                <td>
                    <div class="action-buttons">
                        <button class="action-btn edit" data-id="${teacher.id}">
                            <i class="fas fa-edit"></i>
                        </button>
                        <button class="action-btn delete" data-id="${teacher.id}">
                            <i class="fas fa-trash"></i>
                        </button>
                    </div>
                </td>
            `;

            teachersTableBody.appendChild(row);
        });

        // O'qituvchilar sonini yangilash
        teacherCount.textContent = `${teachersList.length} ta o'qituvchi`;

        // Tahrirlash va o'chirish tugmalariga event listener qo'shish
        attachRowActions();
    }

    // Tahrirlash va o'chirish funksiyalarini ulash
    function attachRowActions() {
        // Tahrirlash tugmalari
        document.querySelectorAll('.action-btn.edit').forEach(btn => {
            btn.addEventListener('click', function() {
                const teacherId = parseInt(this.getAttribute('data-id'));
                openEditModal(teacherId);
            });
        });

        // O'chirish tugmalari
        document.querySelectorAll('.action-btn.delete').forEach(btn => {
            btn.addEventListener('click', function() {
                const teacherId = parseInt(this.getAttribute('data-id'));
                deleteTeacher(teacherId);
            });
        });
    }

    // Qidiruv funksiyasi
    function searchTeachers() {
        const searchTerm = searchInput.value.toLowerCase();
        const filterValue = filterSubject.value;

        let filteredTeachers = teachers.filter(teacher => {
            const fullName = `${teacher.firstName} ${teacher.lastName}`.toLowerCase();
            const email = teacher.email.toLowerCase();

            const matchesSearch = fullName.includes(searchTerm) ||
                                  email.includes(searchTerm) ||
                                  teacher.phone.includes(searchTerm);

            const matchesFilter = filterValue === 'all' || teacher.subject === filterValue;

            return matchesSearch && matchesFilter;
        });

        renderTeachers(filteredTeachers);
    }

    // Yangi o'qituvchi qo'shish modalini ochish
    addTeacherBtn.addEventListener('click', function() {
        addTeacherModal.classList.add('active');
        addTeacherForm.reset();
    });

    // Modal yopish funksiyalari
    function closeModals() {
        addTeacherModal.classList.remove('active');
        editTeacherModal.classList.remove('active');
    }

    closeAddModal.addEventListener('click', closeModals);
    closeEditModal.addEventListener('click', closeModals);
    cancelAdd.addEventListener('click', closeModals);
    cancelEdit.addEventListener('click', closeModals);

    // Modal tashqarisiga bosilganda yopish
    window.addEventListener('click', function(event) {
        if (event.target === addTeacherModal) {
            closeModals();
        }
        if (event.target === editTeacherModal) {
            closeModals();
        }
    });

    // Yangi o'qituvchi qo'shish formasi
    addTeacherForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const newTeacher = {
            id: teachers.length > 0 ? Math.max(...teachers.map(t => t.id)) + 1 : 1,
            firstName: document.getElementById('first-name').value,
            lastName: document.getElementById('last-name').value,
            phone: document.getElementById('phone').value,
            email: document.getElementById('email').value,
            subject: document.getElementById('subject').value,
            status: document.querySelector('input[name="status"]:checked').value,
            notes: document.getElementById('notes').value
        };

        teachers.push(newTeacher);
        renderTeachers();
        closeModals();

        // Muvaffaqiyat xabari
        showNotification('Yangi o\'qituvchi muvaffaqiyatli qo\'shildi!', 'success');
    });

    // O'qituvchini tahrirlash modalini ochish
    function openEditModal(teacherId) {
        const teacher = teachers.find(t => t.id === teacherId);

        if (!teacher) return;

        // Formani to'ldirish
        document.getElementById('edit-id').value = teacher.id;
        document.getElementById('edit-first-name').value = teacher.firstName;
        document.getElementById('edit-last-name').value = teacher.lastName;
        document.getElementById('edit-phone').value = teacher.phone;
        document.getElementById('edit-email').value = teacher.email;
        document.getElementById('edit-subject').value = teacher.subject;
        document.getElementById('edit-notes').value = teacher.notes;

        // Statusni belgilash
        if (teacher.status === 'active') {
            document.getElementById('edit-status-active').checked = true;
        } else {
            document.getElementById('edit-status-inactive').checked = true;
        }

        editTeacherModal.classList.add('active');
    }

    // O'qituvchi ma'lumotlarini yangilash
    editTeacherForm.addEventListener('submit', function(e) {
        e.preventDefault();

        const teacherId = parseInt(document.getElementById('edit-id').value);
        const teacherIndex = teachers.findIndex(t => t.id === teacherId);

        if (teacherIndex !== -1) {
            teachers[teacherIndex] = {
                ...teachers[teacherIndex],
                firstName: document.getElementById('edit-first-name').value,
                lastName: document.getElementById('edit-last-name').value,
                phone: document.getElementById('edit-phone').value,
                email: document.getElementById('edit-email').value,
                subject: document.getElementById('edit-subject').value,
                status: document.querySelector('input[name="edit-status"]:checked').value,
                notes: document.getElementById('edit-notes').value
            };

            renderTeachers();
            closeModals();

            showNotification('O\'qituvchi ma\'lumotlari muvaffaqiyatli yangilandi!', 'success');
        }
    });

    // O'qituvchini o'chirish
    deleteTeacherBtn.addEventListener('click', function() {
        const teacherId = parseInt(document.getElementById('edit-id').value);

        if (confirm('Haqiqatan ham bu o\'qituvchini o\'chirmoqchimisiz?')) {
            teachers = teachers.filter(t => t.id !== teacherId);
            renderTeachers();
            closeModals();

            showNotification('O\'qituvchi muvaffaqiyatli o\'chirildi!', 'success');
        }
    });

    // Modal ichidagi o'chirish funksiyasi
    function deleteTeacher(teacherId) {
        if (confirm('Haqiqatan ham bu o\'qituvchini o\'chirmoqchimisiz?')) {
            teachers = teachers.filter(t => t.id !== teacherId);
            renderTeachers();

            showNotification('O\'qituvchi muvaffaqiyatli o\'chirildi!', 'success');
        }
    }

    // Notification funksiyasi
    function showNotification(message, type = 'info') {
        // Mavjud notificationni olib tashlash
        const existingNotification = document.querySelector('.notification');
        if (existingNotification) {
            existingNotification.remove();
        }

        // Yangi notification yaratish
        const notification = document.createElement('div');
        notification.className =