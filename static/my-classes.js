const classes = [
    {
        name: "10-A sinf",
        subject: "Matematika",
        students: 28,
        lessons: "Haftasiga 4 marta",
        status: "active"
    },
    {
        name: "9-B sinf",
        subject: "Algebra",
        students: 25,
        lessons: "Haftasiga 3 marta",
        status: "active"
    },
    {
        name: "11-C sinf",
        subject: "Geometriya",
        students: 22,
        lessons: "Yakunlangan",
        status: "completed"
    }
];

const grid = document.getElementById("classesGrid");

classes.forEach(cls => {
    const card = document.createElement("div");
    card.className = "class-card";

    card.innerHTML = `
        <div class="class-card-header">
            <div class="class-title">${cls.name}</div>
            <span class="badge ${cls.status}">${cls.status}</span>
        </div>

        <strong>${cls.subject}</strong>

        <div class="class-info">
            <div class="info-item">
                <i class="fas fa-user-graduate"></i>
                ${cls.students} o‘quvchi
            </div>
            <div class="info-item">
                <i class="fas fa-clock"></i>
                ${cls.lessons}
            </div>
        </div>

        <div class="class-footer">
            <button class="btn view">Ko‘rish</button>
            <button class="btn manage">Boshqarish</button>
        </div>
    `;

    grid.appendChild(card);
});
