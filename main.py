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
    test_result = int(testing(x))
    the_answer = int(programm_output[x])

    if test_result==the_answer:
        testing_result = f"Тест {x+1}: Правильно ✅"
    else:
        testing_result = f"Тест {x+1}: Неправильно ❎"
    testing(x)
    resultat.append(testing_result)
    tests_times+=1

resultat[0] = f"Было проведено проверок {tests_times}"

for item in resultat:
    print(item)
