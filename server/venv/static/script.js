let tasks = [];

if (localStorage.getItem('dailyz-tasks')) {
    tasks = JSON.parse(localStorage.getItem('dailyz-tasks'));
}

function saveTasks() {
    localStorage.setItem('dailyz-tasks', JSON.stringify(tasks));
}

function renderTasks() {
    const list = document.getElementById('task-list');
    list.innerHTML = '';
    tasks.forEach((task, index) => {
        const li = document.createElement('li');
        li.className = task.done ? 'completed' : '';
        li.innerHTML = `
            <input type="checkbox" ${task.done ? 'checked' : ''} data-index="${index}">
            <span>${task.text}</span>
            <button data-del="${index}">Удалить</button>
        `;
        list.appendChild(li);
    });
}

function addTask(text) {
    tasks.push({ text, done: false });
    saveTasks();
    renderTasks();
}

document.getElementById('task-form').addEventListener('submit', function(e) {
    e.preventDefault();
    const input = document.getElementById('task-input');
    addTask(input.value);
    input.value = '';
});

document.getElementById('task-list').addEventListener('click', function(e) {
    if (e.target.tagName === 'BUTTON') {
        const idx = e.target.getAttribute('data-del');
        tasks.splice(idx, 1);
        saveTasks();
        renderTasks();
    }
    if (e.target.type === 'checkbox') {
        const idx = e.target.getAttribute('data-index');
        tasks[idx].done = e.target.checked;
        saveTasks();
        renderTasks();
    }
});

renderTasks();
