import os
import re

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks")
PATTERN = re.compile(r'^meta:(\w+)\s*=\s*(.+)$')


def _add_task(tasks: dict, meta: dict) -> None:
    number = meta.get("number")
    if number is None:
        return

    if number.isdigit():
        number = str(int(number))

    tasks[number] = meta


def parse_file(path) -> dict:
    """Читает метаданные задач из .md-файла.

    Возвращает словарь вида {номер задачи: {ключ: значение}}, чтобы задачи
    не перезаписывали друг друга (раньше возвращался один плоский словарь
    и оставались только метаданные последней задачи).
    """
    tasks = {}
    current = {}

    with open(path, encoding="utf-8") as f:
        for line in f:
            m = PATTERN.match(line.strip())
            if not m:
                continue

            key = m.group(1)
            val = m.group(2).split("#")[0].strip()
            val = val.rstrip("\\").strip()
            val = val.strip('"')

            # Повтор ключа внутри блока означает начало метаданных
            # следующей задачи (у каждой задачи свой meta:number).
            if key in current:
                _add_task(tasks, current)
                current = {}

            current[key] = val

    _add_task(tasks, current)
    return tasks
