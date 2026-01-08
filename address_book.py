from pprint import pprint
# читаем адресную книгу в формате CSV в список contacts_list
import csv
import re


def format_phone(match):
  phone = f"+7({match.group(2)}){match.group(3)}-{match.group(4)}-{match.group(5)}"
  if match.group(6):
    phone += f" доб.{match.group(6)}"
  return phone

pattern = r"(\+7|8)[\s\-\(]*(\d{3})[\s\-\)]*(\d{3})[\s\-]*(\d{2})[\s\-]*(\d{2})(?:[\s\(]*(?:доб\.?|ext\.?)[\s\)]*(\d+)[\s\)]*)?"

with open("phonebook_raw.csv", encoding="utf-8-sig") as f:
  rows = csv.reader(f, delimiter=",")
  contacts_list = list(rows)


  for i , contact in enumerate(contacts_list):
    if i == 0:
      continue
    
    fio = contact[:3]
    fio_c = " ".join(fio)
    fio_result = fio_c.split()


    contact[0] = fio_result[0]
    contact[1] = fio_result[1]

    if len(fio_result) > 2:
      contact[2] = fio_result[2]
    else:
      contact[2] = ''

    if len(contact) > 3:
      phone = re.sub(pattern, format_phone, contact[5])
      contact[5] = phone



merged = {}
for contact in contacts_list[1:]:
  key = (contact[0], contact[1])
  if key in merged:
    merged[key] = [merged[key][i] if merged[key][i] else contact[i] for i in range(len(merged[key]))]
  else:
    merged[key] = contact



with open("phonebook.csv", "w", encoding="utf-8") as f:
  datawriter = csv.writer(f, delimiter=',')
  datawriter.writerow(contacts_list[0]) # заголовок
  datawriter.writerows(merged.values())


# Поместить Фамилию, Имя и Отчество человека в поля lastname, firstname и surname соответственно. В записной книжке изначально может быть Ф + ИО, ФИО, а может быть сразу правильно: Ф+И+О. Подсказка: работайте со срезом списка (три первых элемента) при помощи " ".join([:2]) и split(" "), регулярки здесь НЕ НУЖНЫ.
# Привести все телефоны в формат +7(999)999-99-99. Если есть добавочный номер, формат будет такой: +7(999)999-99-99 доб.9999. Подсказка: используйте регулярки для обработки телефонов.
# Объединить все дублирующиеся записи о человеке в одну. Подсказка: группируйте записи по ФИО (если будет сложно, допускается группировать только по ФИ).