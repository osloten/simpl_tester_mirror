from pathlib import Path

json_file = Path('./problems/1.out')

# Проверяем, существует ли файл
if not json_file.exists():
    print(f"❌ Файл не найден: {json_file}")
else:
    # Читаем как обычный текст
    content = json_file.read_text(encoding='utf-8')
    print(f"Размер файла: {len(content)} байт")
    print(f"Содержимое:\n{content}")

    # Если файл пустой
    if not content.strip():
        print("⚠️ Файл пустой!")
