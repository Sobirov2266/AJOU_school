// Dastlabki ma'lumotlar - backenddan keladigan ma'lumotlar o'rniga
const classesData = [
    { id: 1, name: "9-A sinfi", subject: "Matematika", studentCount: 28, lastAttendance: "2023-10-15" },
    { id: 2, name: "9-B sinfi", subject: "Matematika", studentCount: 25, lastAttendance: "2023-10-14" },
    { id: 3, name: "10-A sinfi", subject: "Geometriya", studentCount: 30, lastAttendance: "2023-10-13" },
    { id: 4, name: "10-B sinfi", subject: "Geometriya", studentCount: 26, lastAttendance: "2023-10-12" },
    { id: 5, name: "11-A sinfi", subject: "Algebra", studentCount: 24, lastAttendance: "2023-10-11" },
    { id: 6, name: "11-B sinfi", subject: "Algebra", studentCount: 29, lastAttendance: "2023-10-10" }
];

// O'quvchilar ma'lumotlari (sinflar bo'yicha)
const studentsData = {
    1: [
        { id: 1, name: "Aliyev Aziz", phone: "+998901234567", attendance: null, reason: "" },
        { id: 2, name: "Bekmurodova Dilnoza", phone: "+998902345678", attendance: null, reason: "" },
        { id: 3, name: "Karimov Jasur", phone: "+998903456789", attendance: null, reason: "" },
        { id: 4, name: "Rahimova Madina", phone: "+998904567890", attendance: null, reason: "" },
        { id: 5, name: "To'rayev Sardor", phone: "+998905678901", attendance: null, reason: "" },
        { id: 6, name: "Usmonova Zuhra", phone: "+998906789012", attendance: null, reason: "" },
        { id: 7, name: "Hasanov Olim", phone: "+998907890123", attendance: null, reason: "" },
        { id: 8, name: "Yuldasheva Malika", phone: "+998908901234", attendance: null, reason: "" }
    ],
    2: [
        { id: 1, name: "Qodirov Akmal", phone: "+998911234567", attendance: null, reason: "" },
        { id: 2, name: "Sobirova Nilufar", phone: "+998912345678", attendance: null, reason: "" },
        { id: 3, name: "Tursunov Bekzod", phone: "+998913456789", attendance: null, reason: "" },
        { id: 4, name: "Abdurahmonova Feruza", phone: "+998914567890", attendance: null, reason: "" }
    ],
    3: [
        { id: 1, name: "Omonov Shoxrux", phone: "+998921234567", attendance: null, reason: "" },
        { id: 2, name: "G'aniyeva Sevara", phone: "+998922345678", attendance: null, reason: "" },
        { id: 3, name: "Fayziyev Rustam", phone: "+998923456789", attendance: null, reason: "" }
    ]
};

// Hozirgi holatni saqlash uchun obyekt
let state = {
    selectedClassId: null,
    selectedClass: null,
    attendanceDate: new Date().toISOString().split('T')[0],
    students: [],
    currentStudentForReason: null,
    currentReason: ""
};

// DOM elementlari
let classCardsContainer;
let attendanceSection;
let selectedClassTitle;
let attendanceDateInput;
let backToClassesBtn;
let saveAttendanceBtn;
let attendanceTableBody;
let studentSearchInput;
let markAllPresentBtn;
let markAllAbsentBtn;
let presentCountElem;
let absentCountElem;
let totalCountElem;
let reasonModal;
let closeModalBtn;
let cancelReasonBtn;
let saveReasonBtn;
let studentNameModal;
let customReasonTextarea;
let reasonOptions;
let currentDateElem;

// Dastur ishga tushganda
document.addEventListener('DOMContentLoaded', function() {
    // DOM elementlarini aniqlash
    initializeDOMElements();

    // Joriy sanani ko'rsatish
    updateCurrentDate();

    // Sana tanloviga bugungi sanani o'rnatish
    attendanceDateInput.value = state.attendanceDate;

    // Sinflar kartalarini yaratish
    renderClassCards();

    // Hodisa qayd etish
    setupEventListeners();

    // Boshlang'ich holatni sozlash
    resetModalState();
});

// DOM elementlarini aniqlash
function initializeDOMElements() {
    classCardsContainer = document.getElementById('class-cards');
    attendanceSection = document.getElementById('attendance-section');
    selectedClassTitle = document.getElementById('selected-class-title');
    attendanceDateInput = document.getElementById('attendance-date');
    backToClassesBtn = document.getElementById('back-to-classes');
    saveAttendanceBtn = document.getElementById('save-attendance');
    attendanceTableBody = document.getElementById('attendance-table-body');
    studentSearchInput = document.getElementById('student-search');
    markAllPresentBtn = document.getElementById('mark-all-present');
    markAllAbsentBtn = document.getElementById('mark-all-absent');
    presentCountElem = document.getElementById('present-count');
    absentCountElem = document.getElementById('absent-count');
    totalCountElem = document.getElementById('total-count');
    reasonModal = document.getElementById('reason-modal');
    closeModalBtn = document.getElementById('close-modal');
    cancelReasonBtn = document.getElementById('cancel-reason');
    saveReasonBtn = document.getElementById('save-reason');
    studentNameModal = document.getElementById('student-name-modal');
    customReasonTextarea = document.getElementById('custom-reason');
    reasonOptions = document.querySelectorAll('.reason-option');
    currentDateElem = document.getElementById('current-date');
}

// Joriy sanani yangilash
function updateCurrentDate() {
    const now = new Date();
    const options = { weekday: 'long', year: 'numeric', month: 'long', day: 'numeric' };
    currentDateElem.textContent = now.toLocaleDateString('uz-UZ', options);
}

// Sinflar kartalarini render qilish
function renderClassCards() {
    classCardsContainer.innerHTML = '';

    classesData.forEach(classItem => {
        const classCard = document.createElement('div');
        classCard.className = 'class-card';
        if (state.selectedClassId === classItem.id) {
            classCard.classList.add('active');
        }

        classCard.innerHTML = `
            <div class="class-card-header">
                <div class="class-name">${classItem.name}</div>
                <div class="class-stats">
                    <div class="class-stat">
                        <div class="value">${classItem.studentCount}</div>
                        <div class="label">o'quvchi</div>
                    </div>
                </div>
            </div>
            <div class="class-info">
                <p><i class="fas fa-book"></i> ${classItem.subject}</p>
                <p><i class="fas fa-calendar-check"></i> Oxirgi davomat: ${classItem.lastAttendance}</p>
            </div>
        `;

        classCard.addEventListener('click', () => selectClass(classItem.id));
        classCardsContainer.appendChild(classCard);
    });
}

// Sinf tanlash funksiyasi
function selectClass(classId) {
    state.selectedClassId = classId;
    state.selectedClass = classesData.find(c => c.id === classId);

    // Agar o'quvchilar ma'lumotlari mavjud bo'lsa
    if (studentsData[classId]) {
        state.students = studentsData[classId].map(student => ({...student}));
    } else {
        state.students = [];
    }

    // Sinflar ro'yxatini yangilash
    renderClassCards();

    // Davomat bo'limini ko'rsatish
    attendanceSection.classList.remove('hidden');

    // Scrollni yuqoriga olib chiqish
    attendanceSection.scrollIntoView({ behavior: 'smooth' });

    // Sarlavhani yangilash
    selectedClassTitle.textContent = `${state.selectedClass.name} uchun davomat`;

    // Davomat jadvalini yangilash
    renderAttendanceTable();

    // Hisob-kitoblarni yangilash
    updateSummary();
}

// Davomat jadvalini render qilish
function renderAttendanceTable() {
    attendanceTableBody.innerHTML = '';

    if (state.students.length === 0) {
        attendanceTableBody.innerHTML = `
            <tr>
                <td colspan="5" style="text-align: center; padding: 2rem;">
                    <i class="fas fa-users-slash" style="font-size: 2rem; color: #ccc; margin-bottom: 1rem; display: block;"></i>
                    Ushbu sinfda hozircha o'quvchilar mavjud emas
                </td>
            </tr>
        `;
        return;
    }

    // Qidiruv so'zini olish
    const searchTerm = studentSearchInput.value.toLowerCase();

    // Filtrlangan o'quvchilar ro'yxati
    let filteredStudents = state.students;
    if (searchTerm) {
        filteredStudents = state.students.filter(student =>
            student.name.toLowerCase().includes(searchTerm) ||
            student.phone.includes(searchTerm)
        );
    }

    // Jadval qatorlarini yaratish
    filteredStudents.forEach((student, index) => {
        const row = document.createElement('tr');

        // Davomat holati tugmalari uchun klasslarni aniqlash
        const presentBtnClass = student.attendance === true ? 'status-btn status-present active' : 'status-btn status-present';
        const absentBtnClass = student.attendance === false ? 'status-btn status-absent active' : 'status-btn status-absent';

        // Sabab ko'rsatish uchun kontent
        let reasonContent = '';
        if (student.attendance === false && student.reason) {
            reasonContent = `<span class="reason-display" data-id="${student.id}">${student.reason}</span>`;
        } else if (student.attendance === false) {
            reasonContent = `<span class="reason-display" data-id="${student.id}">Sababni belgilash</span>`;
        }

        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${student.name}</td>
            <td>${student.phone}</td>
            <td>
                <div class="attendance-status">
                    <button class="${presentBtnClass}" data-id="${student.id}" data-status="present">
                        <i class="fas fa-check"></i> Keldi
                    </button>
                    <button class="${absentBtnClass}" data-id="${student.id}" data-status="absent">
                        <i class="fas fa-times"></i> Kelmadi
                    </button>
                </div>
            </td>
            <td class="reason-cell">
                ${reasonContent}
            </td>
        `;

        attendanceTableBody.appendChild(row);
    });

    // Jadvaldagi tugmalar uchun hodisa qayd etish
    attachTableEventListeners();
}

// Jadvaldagi tugmalar uchun hodisa qayd etish
function attachTableEventListeners() {
    // Davomat holati tugmalari
    document.querySelectorAll('.status-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const studentId = parseInt(this.getAttribute('data-id'));
            const status = this.getAttribute('data-status');
            updateAttendanceStatus(studentId, status === 'present');
        });
    });

    // Sabab ko'rsatish tugmalari
    document.querySelectorAll('.reason-display').forEach(btn => {
        btn.addEventListener('click', function() {
            const studentId = parseInt(this.getAttribute('data-id'));
            openReasonModal(studentId);
        });
    });
}

// Davomat holatini yangilash
function updateAttendanceStatus(studentId, isPresent) {
    const student = state.students.find(s => s.id === studentId);
    if (student) {
        student.attendance = isPresent;

        // Agar kelgan bo'lsa, sababni tozalash
        if (isPresent) {
            student.reason = "";
        } else {
            // Agar kelmagan bo'lsa, sabab modalini ochish
            openReasonModal(studentId);
        }

        // Jadvalni yangilash
        renderAttendanceTable();
        updateSummary();
    }
}

// Modal oynasini ochish
function openReasonModal(studentId) {
    const student = state.students.find(s => s.id === studentId);
    if (!student) return;

    state.currentStudentForReason = studentId;
    studentNameModal.textContent = student.name;

    // Agar avval sabab belgilangan bo'lsa
    if (student.reason) {
        customReasonTextarea.value = student.reason;

        // Standart sabablardan birini belgilash
        reasonOptions.forEach(option => {
            if (option.getAttribute('data-reason') === student.reason) {
                option.classList.add('active');
            } else {
                option.classList.remove('active');
            }
        });
    } else {
        resetModalState();
    }

    reasonModal.classList.remove('hidden');
}

// Modal holatini tiklash
function resetModalState() {
    customReasonTextarea.value = '';
    reasonOptions.forEach(option => option.classList.remove('active'));
}

// Hisob-kitoblarni yangilash
function updateSummary() {
    if (state.students.length === 0) {
        presentCountElem.textContent = '0';
        absentCountElem.textContent = '0';
        totalCountElem.textContent = '0';
        return;
    }

    const presentCount = state.students.filter(s => s.attendance === true).length;
    const absentCount = state.students.filter(s => s.attendance === false).length;

    presentCountElem.textContent = presentCount;
    absentCountElem.textContent = absentCount;
    totalCountElem.textContent = state.students.length;
}

// Hodisa qayd etish
function setupEventListeners() {
    // Sana o'zgarishi
    attendanceDateInput.addEventListener('change', function() {
        state.attendanceDate = this.value;
        console.log('Davomat sanasi:', state.attendanceDate);
    });

    // Sinflarga qaytish
    backToClassesBtn.addEventListener('click', function() {
        attendanceSection.classList.add('hidden');
        state.selectedClassId = null;
        state.selectedClass = null;
        renderClassCards();

        // Scrollni yuqoriga olib chiqish
        document.querySelector('.class-selection').scrollIntoView({ behavior: 'smooth' });
    });

    // Davomatni saqlash
    saveAttendanceBtn.addEventListener('click', function() {
        // Faqat kelmagan o'quvchilarni tekshirish
        const absentStudents = state.students.filter(s => s.attendance === false && !s.reason);

        if (absentStudents.length > 0) {
            if (confirm(`${absentStudents.length} ta o'quvchi kelmagan, lekin sababi belgilanmagan. Davom etasizmi?`)) {
                saveAttendanceData();
            }
        } else {
            saveAttendanceData();
        }
    });

    // Barchasini keldi deb belgilash
    markAllPresentBtn.addEventListener('click', function() {
        if (state.students.length === 0) return;

        if (confirm(`Barcha ${state.students.length} ta o'quvchini keldi deb belgilasizmi?`)) {
            state.students.forEach(student => {
                student.attendance = true;
                student.reason = "";
            });
            renderAttendanceTable();
            updateSummary();
        }
    });

    // Barchasini kelmadi deb belgilash
    markAllAbsentBtn.addEventListener('click', function() {
        if (state.students.length === 0) return;

        if (confirm(`Barcha ${state.students.length} ta o'quvchini kelmadi deb belgilasizmi?`)) {
            state.students.forEach(student => {
                student.attendance = false;
            });
            renderAttendanceTable();
            updateSummary();
        }
    });

    // O'quvchi qidirish
    studentSearchInput.addEventListener('input', function() {
        renderAttendanceTable();
    });

    // Modal oynasi uchun hodisalar
    closeModalBtn.addEventListener('click', closeReasonModal);
    cancelReasonBtn.addEventListener('click', closeReasonModal);

    // Sabab tanlash
    reasonOptions.forEach(option => {
        option.addEventListener('click', function() {
            // Barcha tanlovlardan faol klassni olib tashlash
            reasonOptions.forEach(opt => opt.classList.remove('active'));

            // Tanlangan elementga faol klassni qo'shish
            this.classList.add('active');

            // Textarea ni tozalash
            customReasonTextarea.value = '';
        });
    });

    // Sababni saqlash
    saveReasonBtn.addEventListener('click', saveReason);

    // Modal tashqarisiga bosganda yopish
    reasonModal.addEventListener('click', function(e) {
        if (e.target === reasonModal) {
            closeReasonModal();
        }
    });

    // Escape tugmasi bilan modalni yopish
    document.addEventListener('keydown', function(e) {
        if (e.key === 'Escape' && !reasonModal.classList.contains('hidden')) {
            closeReasonModal();
        }
    });
}

// Modal oynasini yopish
function closeReasonModal() {
    reasonModal.classList.add('hidden');
    state.currentStudentForReason = null;
    resetModalState();
}

// Sababni saqlash
function saveReason() {
    const studentId = state.currentStudentForReason;
    const student = state.students.find(s => s.id === studentId);

    if (!student) {
        closeReasonModal();
        return;
    }

    // Tanlangan sababni aniqlash
    let reason = '';
    const selectedOption = document.querySelector('.reason-option.active');

    if (selectedOption) {
        reason = selectedOption.getAttribute('data-reason');
    } else if (customReasonTextarea.value.trim()) {
        reason = customReasonTextarea.value.trim();
    }

    // Agar sabab tanlanmagan bo'lsa
    if (!reason) {
        alert("Iltimos, sababni tanlang yoki kiriting!");
        return;
    }

    // Sababni saqlash
    student.reason = reason;

    // Modalni yopish va jadvalni yangilash
    closeReasonModal();
    renderAttendanceTable();
    updateSummary();
}

// Davomat ma'lumotlarini saqlash (simulyatsiya)
function saveAttendanceData() {
    // Ma'lumotlarni tayyorlash
    const attendanceData = {
        classId: state.selectedClassId,
        className: state.selectedClass ? state.selectedClass.name : '',
        date: state.attendanceDate,
        students: state.students.map(student => ({
            id: student.id,
            name: student.name,
            attendance: student.attendance,
            reason: student.reason
        }))
    };

    // Bu yerda backendga so'rov yuboriladi
    console.log('Davomat ma\'lumotlari saqlandi:', attendanceData);

    // Foydalanuvchiga xabar
    alert(`Davomat ma'lumotlari saqlandi!\n\nSana: ${state.attendanceDate}\nSinf: ${state.selectedClass.name}\nKeldi: ${presentCountElem.textContent}\nKelmadi: ${absentCountElem.textContent}`);

    // Ma'lumotlarni saqlashdan keyin sinflarga qaytish
    backToClassesBtn.click();
}