// Dlaždice v menu
function showSubtiles(sectionId) {
    document.querySelector('#main-tiles').style.display = 'none';
    document.querySelector('#subtiles').style.display = 'block';
    document.querySelectorAll('#subtiles .tiles').forEach(group => {
        group.style.display = 'none';
    });

    const target = document.querySelector(`#${sectionId}`);
    if (target) {
        target.style.display = 'grid';
    }
}

// Tlačítko zpět u dlaždic
function backToMain() {
    document.querySelector('#subtiles').style.display = 'none';
    document.querySelector('#main-tiles').style.display = 'grid';
    document.querySelectorAll('#subtiles .tiles').forEach(group => {
        group.style.display = 'none';
    });
}

// Kalendář
document.addEventListener("DOMContentLoaded", function() {
    const prevBtn = document.getElementById("prev-month");
    const nextBtn = document.getElementById("next-month");
    const calendarTitle = document.getElementById("calendar-title");
    const calendarBody = document.getElementById("calendar-body");
    let currentDate = new Date();

    function renderCalendar(year, month) {
        fetch(`?year=${year}&month=${month + 1}`, {
                headers: {
                    "X-Requested-With": "XMLHttpRequest"
                }
            })
            .then(response => response.json())
            .then(data => {
                calendarTitle.textContent = `${data.month_name} ${data.year}`;
                calendarBody.innerHTML = "";

                data.weeks.forEach(week => {
                    week.forEach(day => {
                        const div = document.createElement("div");
                        div.classList.add("calendar-day");

                        if (day === 0) {
                            div.classList.add("empty");
                        } else {
                            div.textContent = day;
                            div.dataset.day = day;

                            if (
                                day === data.today_day &&
                                data.month === data.today_month &&
                                data.year === data.today_year
                            ) {
                                div.classList.add("today");
                                div.classList.add("selected");
                            }

                            div.addEventListener("click", () => {
                                document.querySelectorAll(".calendar-day.selected").forEach(el => {
                                    el.classList.remove("selected");
                                });
                                div.classList.add("selected");
                                const selectedText = `Vybrané datum: ${day}.${data.month}.${data.year}`;
                                document.getElementById("selected-date").textContent = selectedText;
                            });
                        }
                        calendarBody.appendChild(div);
                    });
                });
            });
    }
    prevBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() - 1);
        renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
    });

    nextBtn.addEventListener("click", () => {
        currentDate.setMonth(currentDate.getMonth() + 1);
        renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
    });
    renderCalendar(currentDate.getFullYear(), currentDate.getMonth());
});

// Budovy a místnosti s checkboxy
document.addEventListener("DOMContentLoaded", function () {
    const tooltip = document.createElement("div");
    tooltip.className = "tooltip";
    document.body.appendChild(tooltip);

    document.querySelectorAll(".building").forEach(building => {
        const checkbox = building.querySelector(".building-checkbox");
        const b = building.dataset.building;
        const roomList = document.querySelector(`.room-list[data-for="${b}"]`);
        let isExpanded = false;

        building.addEventListener("mouseenter", () => {
            tooltip.style.opacity = 1;
        });

        building.addEventListener("mouseleave", () => {
            tooltip.style.opacity = 0;
        });

        building.addEventListener("mousemove", (e) => {
            tooltip.style.left = `${e.pageX + 10}px`;
            tooltip.style.top = `${e.pageY + 10}px`;
            tooltip.textContent = isExpanded ? "🡣 Skrýt místnosti" : "🡡 Zobrazit místnosti";
        });

        building.addEventListener("click", (e) => {
            if (e.target === checkbox) return;

            isExpanded = !isExpanded;
            roomList.classList.toggle("expanded", isExpanded);

            tooltip.textContent = isExpanded ? "🡣 Skrýt místnosti" : "🡡 Zobrazit místnosti";
        });

        checkbox.addEventListener("change", () => {
            const isChecked = checkbox.checked;
            building.classList.toggle("selected", isChecked);

            if (roomList) {
                roomList.querySelectorAll(".room").forEach(room => {
                    const roomCheckbox = room.querySelector(".room-checkbox");
                    roomCheckbox.checked = isChecked;
                    room.classList.toggle("selected", isChecked);
                });
            }
        });
    });

    document.querySelectorAll(".room").forEach(room => {
        const checkbox = room.querySelector(".room-checkbox");

        room.addEventListener("click", (e) => {
            e.stopPropagation();
            checkbox.checked = !checkbox.checked;
            room.classList.toggle("selected", checkbox.checked);
        });

        checkbox.addEventListener("click", (e) => {
            e.stopPropagation();
        });

        checkbox.addEventListener("change", () => {
            room.classList.toggle("selected", checkbox.checked);
        });
    });
});
