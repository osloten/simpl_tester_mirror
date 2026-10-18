import os
import re

TASKS_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "tasks")
PATTERN = re.compile(r'^meta:(\w+)\s*=\s*(.+)$')


def parse_file(path):
    meta = {}
    with open(path, encoding="utf-8") as f:
        for line in f:
            m = PATTERN.match(line.strip())
            if not m:
                continue

            key = m.group(1)
            val = m.group(2).split("#")[0].strip()
            val = val.rstrip("\\").strip()
            val = val.strip('"')

            meta[key] = val
    return meta
