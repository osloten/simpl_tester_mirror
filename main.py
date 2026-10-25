# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import sys
from pathlib import Path
from subprocess import check_output
from time import perf_counter

from core.data_parser import parse_data
from core.fetch import fetch_olympiads
from core.info_parser import parse_file

parser = argparse.ArgumentParser(description="Тестировщик олимпиадных задач")
parser.add_argument("olympiad", help="Название папки с олимпиадой")
parser.add_argument("--fetch", action="store_true", help="Скачать олимпиады из репозитория (можно без названия олимпиады)")
args = parser.parse_args()
number = int(input("Номер задачи "))
this_folder = Path(__file__).parent.resolve()
target_folder = this_folder / 'tests' / args.olympiad
existing_extensions = {f.suffix for f in target_folder.glob(f"{number}.*")}
tasks_info = parse_file(this_folder / 'tasks' / f"{args.olympiad}.md")
task_info = tasks_info.get(str(number))

if task_info is None:
    print(f"В tasks/{args.olympiad}.md нет задачи с номером {number}.")
    sys.exit(1)

if args.fetch:
    rc = fetch_olympiads()
    if rc != 0:
        sys.exit(rc)
    if not args.olympiad:
        sys.exit(0)

if not args.olympiad:
    print("Укажите название олимпиады или используйте --fetch.")
    sys.exit(1)

input_path = Path(this_folder) / task_info.get('stdin', f"problems/{args.olympiad}/{number}.in")
output_path = Path(this_folder) / task_info.get('stdout', f"problems/{args.olympiad}/{number}.out")

for path in (input_path, output_path):
    if not path.is_file():
        print(f"Не найден файл с тестами: {path}")
        sys.exit(1)

programm_input = parse_data(str(input_path))
programm_output = parse_data(str(output_path))

if not programm_input:
    print(f"Файл с тестами пуст: {input_path}")
    sys.exit(1)

if len(programm_input) != len(programm_output):
    print(
        f"Количество тестов не совпадает: {len(programm_input)} в {input_path.name} "
        f"и {len(programm_output)} в {output_path.name}."
    )
    sys.exit(1)


def testing_py(target_script, data: str) -> str:
    return check_output(
        ["python", str(target_script)],
        input=data + "\n",
        text=True,
        encoding='utf8',
        timeout=10.0
    ).strip()


def testing_bin(target_script, data: str) -> str:
    return check_output(
        [target_script],
        input=data + "\n",
        text=True,
        encoding='utf8',
        timeout=10.0
    ).strip()

choosen_func = testing_py

if ".py" in existing_extensions:
    target_script = target_folder / f"{number}.py"
    choosen_func = testing_py
elif sys.platform == "win32" and ".exe" in existing_extensions:
    target_script = target_folder / f"{number}.exe"
    choosen_func = testing_bin
elif sys.platform.startswith(("linux", "darwin")) and (target_folder / str(number)).is_file():
    target_script = target_folder / str(number)
    choosen_func = testing_bin
else:
    print("Я не вижу подходящих файлов в tests! Пожалуйста, создайте .py скрипт или скомпилированный файл.")
    sys.exit(1)

tests_times = 0
resultat = ["Результаты:"]

all_time = []

for test_number in programm_input:
    start_time = perf_counter()
    test_result = str(choosen_func(target_script, programm_input[test_number])).strip()
    the_answer = str(programm_output[test_number]).strip()

    answer_display = the_answer.replace("\n", " ")
    result_display = test_result.replace("\n", " ")

    if test_result == the_answer:
        testing_result = f"Тест {test_number}: \033[32mПравильно ✅\033[0m (ожидалось: {answer_display}, получили: {result_display})"
    else:
        testing_result = f"Тест {test_number}: \033[31mНеправильно ❌\033[0m (ожидалось: {answer_display}, получили: {result_display})"
    resultat.append(testing_result)
    tests_times += 1

    end_time = perf_counter()
    execution_time = end_time - start_time
    all_time.append(execution_time)

last_time = sum(all_time) / len(all_time)


def test_time(time: float, info: dict) -> str:
    limit = info.get('time_limit')

    if limit is None:
        return "лимит времени в метаданных не указан."

    if time <= float(limit):
        right_time_res = f"требовалось: {limit} сек. Во времени уложились!"
    else:
        right_time_res = f"требовалось: {limit} сек. Во времени не уложились, попробуйте оптимизировать!"

    return right_time_res


if last_time < 1:
    resultat.append(f"Среднее время выполнения: {last_time * 1000:.1f} мс, " + test_time(last_time, task_info))
else:
    resultat.append(f"Среднее время выполнения: {last_time:.2f} сек, " + test_time(last_time, task_info))

resultat[0] = f"Было проведено проверок {tests_times}"


for item in resultat:
    print(item)
