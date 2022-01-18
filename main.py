import gspread
import time
from datetime import datetime
import functools
import collections
import numpy as np
from dadata import Dadata
import psycopg2


#необходимо установить: pip install gspread / pip install numpy / pip install Dadata / psycopg2
# sht1 = gc.open_by_key('6937e74677ac5eb0b52f9aa61711856a5940e7d9')
# sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1suZrCDCkxA4T2z67yxZFryVBsf0Qx-x1hE4BF4Ggzks')


def main():
    last = time.time()
    count = 3
    while True:
        if time.time() - last >= 10:
            last = time.time()
            values_list_col1 = worksheet.col_values(1) # список со значениями из первой колонки
            values_list_col2 = worksheet.col_values(2) # список со значениями из второй колонки

            for i in values_list_col1[2:]: # строки с ИНН (i)
                # в result идет массив со всей информацией по организации:
                result = dadata.find_by_id("party", str(i))

                if result:
                    # в переменных сохраняются имя и адрес:
                    row_name_org = result[0]['value']
                    row_address = result[0]['data']['address']['value']
                    print('---------------', row_name_org, '**********', row_address, '---------------')
                    val_col_row = worksheet.cell(count, 3).value # получение значения ячейки

                    # !потом сделать привязку по ИНН к имени и адресу
                    # обновляет значения столбцов 3 и 4 по ИНН:
                    worksheet.update_cell(count, 3, row_name_org)
                    worksheet.update_cell(count, 4, row_address)

                    count += 1
                    if count == (len(values_list_col1) + 1):
                        count = 3


            array_1 = np.array(save_first_list)
            array_2 = np.array(values_list_col1)

            difference_1 = np.setdiff1d(array_1, array_2)
            difference_2 = np.setdiff1d(array_2, array_1)

            list_difference = np.concatenate((difference_1, difference_2))
            print('СПИСОК ИЗМЕНЕНИЙ', list(list_difference), '<--')
            if collections.Counter(values_list_col1) == collections.Counter(save_first_list):
                print("нет изменений")
            else:
                print("есть новые изменения")


print('START')


# соединение с БД:
try:
    db = psycopg2.connect(dbname="da1k16rlco7nqo", user="rorpgbnciyvrdh", password="7c11f860c1f4ef82fa7f23cd2b830ed18fb46c7ac682bbd922ebd0c2f2873e4a", host="ec2-52-211-158-144.eu-west-1.compute.amazonaws.com")
except:
    print("Нет соединения с БД")


cur = db.cursor()
cur.execute("""select * from google_table_test_task""")
rows = cur.fetchall()

cur2 = db.cursor()
cur3 = db.cursor()
inn_list = []

for row in rows:
    inn_list.append(row[1])
    print("   ", row[0], "   ", row[3], "   ", row[4])

# Dadata API:
token = "9489708e7c8c23a62ccbd1182068f13aa12eb801"
dadata = Dadata(token)
# Dadata API END

# путь к JSON Google table
gc = gspread.service_account(filename='test-task-338206-9fc568eb165d.json')
# Открываем тестовую таблицу
sh = gc.open("test table")


worksheet = sh.get_worksheet(0)
values_list_col1 = worksheet.col_values(1)
save_first_list = values_list_col1
list_of_lists = worksheet.get_all_values()
for i in list_of_lists[2:]:
    if i[0] not in inn_list:
        cur2.execute(f"insert into google_table_test_task(inn, kpp, name, address) values('{i[0]}', '{i[1]}', '{i[2]}', '{i[3]}')")
cur3.execute("DELETE FROM google_table_test_task WHERE (id = 11);")
db.commit()


if __name__ == "__main__":
    main()