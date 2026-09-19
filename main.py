# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import json
from pathlib import Path
from subprocess import check_output

number = int(input("Номер задачи "))
this_folder = Path(__file__).parent.resolve()
target_script = this_folder / 'tests' / f'{number}.py'

with open(this_folder / 'problems' / f'{number}.in', "r", encoding="utf-8") as f:
     programm_input:list = json.load(f)

with open(this_folder / 'problems' / f'{number}.out', "r", encoding="utf-8") as f:
     programm_output:list = json.load(f)

def testing(numb:int) -> str:
    return check_output(
        ["python", str(target_script)],
        input=str(programm_input[numb]),
        text=True,
        encoding='utf8'
    ).strip()

tests_times = 0
resultat = [f"Было проведено проверок ({tests_times})", "Результаты:"]


for x in range(len(programm_input)):
    test_result = testing(x).strip()
    the_answer = programm_output[x].strip()

    if test_result==the_answer:
        testing_result = f"Тест {x+1}: \033[32mПравильно ✅\033[0m"
    else:
        testing_result = f"Тест {x+1}: \033[31mНеправильно ❌\033[0m"
    resultat.append(testing_result)
    tests_times+=1

resultat[0] = f"Было проведено проверок {tests_times}"

for item in resultat:
    print(item)
