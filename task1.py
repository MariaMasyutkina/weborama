from zipfile import ZipFile
import os
import shutil
import csv

# получаем текущую папку
cur_dir = os.path.dirname(os.path.abspath(__file__))
file_list = os.listdir(cur_dir)
zip_file = ""

# находим архив в текущей папке
for zip_file in file_list:
    file_name, file_ext = os.path.splitext(zip_file)
    if file_ext == ".zip":
        break

csv_dir = cur_dir + "\\zip_" + file_name

# распаковываем архив
with ZipFile(cur_dir + "\\" + zip_file) as zip:
    zip.extractall(csv_dir)

csv_file = os.listdir(csv_dir)
id_dict = dict()

# открываем csv
with open(csv_dir + "\\" + csv_file[0]) as csv_file:
    reader = csv.reader(csv_file, delimiter=",")
    next(reader)

    # перебираем строки и создаем словарь формата {id: кол-во повторений}
    for line in reader:
        if id_dict.get(line[1]):
            id_dict.update({line[1]: id_dict.get(line[1]) + 1})
        else:
            id_dict.setdefault(line[1], 1)


print("Id, которые встречаются только 3 раза:")
for item in id_dict.items():
    print(item[0]) if item[1] == 3 else next


print("Частота повторений уникальных Id:")
seq = set()
for value in id_dict.values():
    seq.add(value)

seq = dict.fromkeys(seq, 0)

for item in id_dict.items():
    seq.update({item[1]: seq.get(item[1]) + 1})

print(seq)

# удаление распакованной папки
shutil.rmtree(cur_dir + "\\zip_" + file_name)
