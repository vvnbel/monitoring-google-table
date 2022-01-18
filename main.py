import gspread
import time
from datetime import datetime
import functools
import collections
import numpy as np
from dadata import Dadata
import psycopg2
import urllib.parse as urlparse
import os
#необходимо установить: pip install gspread / pip install numpy / pip install Dadata



def main():
    last = time.time()
    count = 3
    while True:
        if time.time() - last >= 10:
            last = time.time()
            values_list_col1 = worksheet.col_values(1)
            values_list_col2 = worksheet.col_values(2)


            for i in values_list_col1[2:]:
                # в результат сохраняются строки с ИНН (i)
                result = dadata.find_by_id("party", str(i))
                if result:
                    row_name_org = result[0]['value']
                    row_address = result[0]['data']['address']['value']
                    print(row_name_org, row_address)
                    val_col_row = worksheet.cell(count, 3).value
                    # когда не принимает значения с dadata то вставляет не правильно
                    # сделать привязку по ИНН к имени и адресу
                    if worksheet.cell(count, 3).value:
                        worksheet.update_cell(count, 3, row_name_org)
                        print('OK')
                    else:
                        print('EMPTY SLOT 3')
                    worksheet.update_cell(count, 4, row_address)
                    count += 1
                    if count == (len(values_list_col1) + 1):
                        count = 3
                    print(val_col_row)


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


            print('первая ячейка', values_list_col1[2:])
            print('вторая ячейка', values_list_col2[2:])

print('START')



try:
    db = psycopg2.connect(dbname="da1k16rlco7nqo", user="rorpgbnciyvrdh", password="7c11f860c1f4ef82fa7f23cd2b830ed18fb46c7ac682bbd922ebd0c2f2873e4a", host="ec2-52-211-158-144.eu-west-1.compute.amazonaws.com")
except:
    print("I am unable to connect to the database")
cur = db.cursor()
cur.execute("""select * from google_table""")

rows = cur.fetchall()

for row in rows:
    print("   ", row[0])
cur2 = db.cursor()
cur2.execute("""insert into google_table(id, Address) values(4, '444')""")
print(cur2)


# Dadata API:
token = "9489708e7c8c23a62ccbd1182068f13aa12eb801"
dadata = Dadata(token)
#result = dadata.find_by_id("party", "4027039637")
#print(result[0]['value'])
#print(result[0]['data']['address']['value'])
# Dadata API END

# путь к JSON Google table
gc = gspread.service_account(filename='test-task-338206-9fc568eb165d.json')
# Открываем тестовую таблицу
sh = gc.open("test table")
# sht1 = gc.open_by_key('6937e74677ac5eb0b52f9aa61711856a5940e7d9')
# sht2 = gc.open_by_url('https://docs.google.com/spreadsheets/d/1suZrCDCkxA4T2z67yxZFryVBsf0Qx-x1hE4BF4Ggzks')

#
worksheet = sh.get_worksheet(0)
values_list_col1 = worksheet.col_values(1)
save_first_list = values_list_col1

# ****этот блок кода тестовый ,можно удалить***********

val = worksheet.acell('A1').value
val2 = worksheet.cell(1, 3).value
values_list = worksheet.row_values(3)
values_list_col = worksheet.col_values(1)
worksheet_list = sh.worksheets() # список листов документа
list_of_lists = worksheet.get_all_values()
# *******************************************************

if __name__ == "__main__":
    main()