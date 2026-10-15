# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import json
import sys
from pathlib import Path
from subprocess import check_output
from time import perf_counter

# from core.parser import parse_file

parser = argparse.ArgumentParser(description="Тестировщик олимпиадных задач")
parser.add_argument("olympiad", help="Название папки с олимпиадой")
args = parser.parse_args()
number = int(input("Номер задачи "))
this_folder = Path(__file__).parent.resolve()
target_folder = this_folder / 'tests' / args.olympiad
existing_extensions = {f.suffix for f in target_folder.glob(f"{number}.*")}
# task_info = parse_file(f"tasks/{args.olympiad}")
target_script = target_folder / f"{number}.py"

with open(this_folder / 'problems' / args.olympiad / f'{number}.in', "r", encoding="utf-8") as f:
     programm_input:list = json.load(f)

with open(this_folder / 'problems' / args.olympiad / f'{number}.out', "r", encoding="utf-8") as f:
     programm_output:list = json.load(f)


def testing_py(numb:int, target_script) -> str:
    return check_output(
        ["python", str(target_script)],
        input=str(programm_input[numb]),
        text=True,
        encoding='utf8'
    ).strip()


def testing_bin(numb:int, target_script) -> str:
    return check_output(
        [target_script],
        input=str(programm_input[numb]),
        text=True,
        encoding='utf8'
    ).strip()

choosen_func = testing_py

if ".py" in existing_extensions:
    target_script = target_folder / f"{number}.py"
    choosen_func = testing_py
elif sys.platform == "win32" and ".exe" in existing_extensions:
    target_script = target_folder / f"{number}.exe"
    choosen_func = testing_bin
elif sys.platform == "darwin" or sys.platform.startswith("linux"):
    target_script = target_folder / f"{number}"
    choosen_func = testing_bin
else:
    print("Я не вижу подходящих файлов в tests/! Пожалуйста, создайте .py скрипт или скомпилированный файл.")
    sys.exit(1)

tests_times = 0
resultat = [f"Было проведено проверок ({tests_times})", "Результаты:"]

all_time = []


for x in range(len(programm_input)):
    start_time = perf_counter()
    test_result = str(choosen_func(x, target_script)).strip()
    the_answer = str(programm_output[x]).strip()

    if test_result==the_answer:
        testing_result = f"Тест {x+1}: \033[32mПравильно ✅\033[0m (ожидалось: {the_answer}, получили: {test_result})"
    else:
        testing_result = f"Тест {x+1}: \033[31mНеправильно ❌\033[0m (ожидалось: {the_answer}, получили: {test_result})"
    resultat.append(testing_result)
    tests_times+=1

    end_time = perf_counter()
    execution_time = end_time - start_time
    all_time.append(execution_time)

last_time = sum(all_time)/len(all_time)
if last_time<1:
    last_time*=1000
    resultat.append(f"Среднее время выполнения: {last_time:.1f} мс")
else:
    resultat.append(f"Среднее время выполнения: {last_time:.2f} сек")

resultat[0] = f"Было проведено проверок {tests_times}"


for item in resultat:
    print(item)
