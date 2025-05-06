// --- Переменные ---
let categories = {
    "Личное": []
};
let selectedCategory = "Личное";
let theme = "light";

// --- Элементы DOM ---
const noteInput = document.getElementById('note-input');
const addNoteBtn = document.getElementById('add-note-btn');
const noteList = document.getElementById('note-list');
const categorySelect = document.getElementById('category-select');
const addCategoryBtn = document.getElementById('add-category-btn');
const newCategoryInput = document.getElementById('new-category-input');
const toggleThemeBtn = document.getElementById('toggle-theme-btn');

// --- Сохранение/загрузка данных ---
function saveData() {
    localStorage.setItem('noteAppData', JSON.stringify({
        categories, selectedCategory, theme
    }));
}

function loadData() {
    const d = JSON.parse(localStorage.getItem('noteAppData') || 'null');
    if(d) {
        categories = d.categories;
        selectedCategory = d.selectedCategory;
        theme = d.theme || 'light';
    }
}
loadData();

// --- Работа с заметками ---
function render() {
    // Категории
    categorySelect.innerHTML = "";
    for (const cat in categories) {
        let opt = document.createElement('option');
        opt.value = cat;
        opt.textContent = cat;
        if(cat === selectedCategory) opt.selected = true;
        categorySelect.appendChild(opt);
    }

    // Список заметок
    noteList.innerHTML = "";
    (categories[selectedCategory] || []).forEach((note, idx) => {
        let li = document.createElement('li');
        li.textContent = note;
        let delBtn = document.createElement('button');
        delBtn.textContent = "Удалить";
        delBtn.onclick = () => {
            categories[selectedCategory].splice(idx, 1);
            saveData();
            render();
        };
        li.appendChild(delBtn);
        noteList.appendChild(li);
    });

    // Очистка поля
    noteInput.value = "";
    newCategoryInput.value = "";
    applyTheme();
}

// --- Добавить заметку ---
addNoteBtn.onclick = () => {
    const note = noteInput.value.trim();
    if(note) {
        categories[selectedCategory].push(note);
        saveData();
        render();
    }
};

// --- Сменить категорию ---
categorySelect.onchange = () => {
    selectedCategory = categorySelect.value;
    saveData();
    render();
};

// --- Добавить категорию ---
addCategoryBtn.onclick = () => {
    const newCat = newCategoryInput.value.trim();
    if(newCat && !(newCat in categories)) {
        categories[newCat] = [];
        selectedCategory = newCat;
        saveData();
        render();
    }
};

// --- Темная тема ---
toggleThemeBtn.onclick = () => {
    theme = theme === 'light' ? 'dark' : 'light';
    saveData();
    render();
};

function applyTheme() {
    if(theme === 'dark') {
        document.body.classList.add('dark');
    } else {
        document.body.classList.remove('dark');
    }
    if(toggleThemeBtn)
        toggleThemeBtn.textContent = theme === 'dark' ? "☀️" : "🌙";
}

// Первая отрисовка
render();
