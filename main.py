# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import argparse
import sys
from pathlib import Path
from subprocess import check_output
from time import perf_counter

from core.data_parser import parse_data
from core.info_parser import parse_file

parser = argparse.ArgumentParser(description="Тестировщик олимпиадных задач")
parser.add_argument("olympiad", help="Название папки с олимпиадой")
args = parser.parse_args()
number = int(input("Номер задачи "))
this_folder = Path(__file__).parent.resolve()
target_folder = this_folder / 'tests' / args.olympiad
existing_extensions = {f.suffix for f in target_folder.glob(f"{number}.*")}
task_info = parse_file(f"tasks/{args.olympiad}.md")
target_script = target_folder / f"{number}.py"


programm_input = parse_data(f"{this_folder}/problems/{args.olympiad}/{number}.in")
programm_output = parse_data(f"{this_folder}/problems/{args.olympiad}/{number}.out")

def testing_py(numb:int, target_script) -> str:
    return check_output(
        ["python", str(target_script)],
        input=programm_input[numb]+"\n",
        text=True,
        encoding='utf8',
        timeout=10.0
    ).strip()


def testing_bin(numb:int, target_script) -> str:
    return check_output(
        [target_script],
        input=programm_input[numb]+"\n",
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
elif sys.platform == "darwin" or sys.platform.startswith("linux"):
    target_script = target_folder / f"{number}"
    choosen_func = testing_bin
else:
    print("Я не вижу подходящих файлов в tests! Пожалуйста, создайте .py скрипт или скомпилированный файл.")
    sys.exit(1)

tests_times = 0
resultat = [f"Было проведено проверок ({tests_times})", "Результаты:"]

all_time = []


for x in range(len(programm_input)):
    start_time = perf_counter()
    test_result = str(choosen_func(x+1, target_script)).strip()
    the_answer = str(programm_output[x+1]).strip()

    if test_result==the_answer:
        testing_result = f"Тест {x+1}: \033[32mПравильно ✅\033[0m (ожидалось: {the_answer.replace('\n', ' ')}, получили: {test_result.replace('\n', ' ')})"
    else:
        testing_result = f"Тест {x+1}: \033[31mНеправильно ❌\033[0m (ожидалось: {the_answer.replace('\n', ' ')}, получили: {test_result.replace('\n', ' ')})"
    resultat.append(testing_result)
    tests_times+=1

    end_time = perf_counter()
    execution_time = end_time - start_time
    all_time.append(execution_time)

last_time = sum(all_time)/len(all_time)

def test_time(time:float=last_time, info:dict=task_info) -> str:
    if time<=float(info['time_limit']):
        right_time_res = f"требовалось: {info['time_limit']} сек. Во времени уложились!"
    else:
        right_time_res = f"требовалось: {info['time_limit']} сек. Во времени не уложились, попробуйте оптимизировать!"

    return right_time_res


if last_time<1:
    last_time*=1000
    resultat.append(f"Среднее время выполнения: {last_time:.1f} мс, " + test_time())
else:
    resultat.append(f"Среднее время выполнения: {last_time:.2f} сек, " + test_time())

resultat[0] = f"Было проведено проверок {tests_times}"


for item in resultat:
    print(item)
