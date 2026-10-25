# This Source Code Form is subject to the terms of the Mozilla Public
# License, v. 2.0. If a copy of the MPL was not distributed with this
# file, You can obtain one at https://mozilla.org/MPL/2.0/.
import io
import json
import sys
import urllib.request
import zipfile
from pathlib import Path

REPO = "https://codeberg.org/oslot/olympiads"
REF = "main"


def fetch_olympiads(root=None, repo=REPO, ref=REF) -> int:
    """Скачивает олимпиады из olympiads.json в <root>/tasks и <root>/problems.

    root=None — взять корень проекта относительно этого файла.
    Возвращает 0 при успехе, 1 при ошибке.
    """
    if root is None:
        root = Path(__file__).parent.parent.resolve()
    else:
        root = Path(root).resolve()

    url = f"{repo}/archive/{ref}.zip"
    print(f"Скачиваю {url}")
    try:
        data = urllib.request.urlopen(url).read()
    except Exception as e:  # noqa: BLE001
        print(f"Не удалось скачать архив: {e}")
        return 1

    try:
        zf = zipfile.ZipFile(io.BytesIO(data))
    except zipfile.BadZipFile as e:
        print(f"Архив повреждён: {e}")
        return 1

    prefix = zf.namelist()[0].split("/", 1)[0] + "/"

    try:
        olympiads = json.loads(zf.read(prefix + "olympiads.json"))
    except (KeyError, json.JSONDecodeError) as e:
        print(f"Не удалось прочитать olympiads.json: {e}")
        return 1

    for name in olympiads:
        try:
            task_src = prefix + f"tasks/{name}.md"
            task_dst = root / "tasks" / f"{name}.md"
            task_dst.parent.mkdir(parents=True, exist_ok=True)
            task_dst.write_bytes(zf.read(task_src))
            print(f"-> {task_dst}")
        except KeyError:
            print(f"В архиве нет tasks/{name}.md, пропускаю {name}")
            continue

        prob_prefix = prefix + f"problems/{name}/"
        for member in zf.namelist():
            if not member.startswith(prob_prefix) or member.endswith("/"):
                continue
            dst = root / "problems" / name / member[len(prob_prefix):]
            dst.parent.mkdir(parents=True, exist_ok=True)
            dst.write_bytes(zf.read(member))
            print(f"-> {dst}")

    print("Готово")
    return 0


if __name__ == "__main__":
    sys.exit(fetch_olympiads())
