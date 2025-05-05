import requests
from tkinter import *

def fetch_tasks():
    resp = requests.get('http://localhost:5000/api/tasks')
    for task in resp.json():
        listbox.insert(END, f'{task["task"]} (Выполнено: {task["done"]})')

root = Tk()
root.title("ToDo Приложение")

listbox = Listbox(root, width=40)
listbox.pack(pady=20)

Button(root, text="Загрузить задачи", command=fetch_tasks).pack()

root.mainloop()
