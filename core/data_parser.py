def parse_data(path: str) -> dict:
    result = {}
    key = 1
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            result[key] = '\n'.join(line.split())
            key += 1
    return result
