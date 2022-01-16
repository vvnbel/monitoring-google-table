import gspread
import time
from datetime import datetime
import functools
import collections
import numpy as np


def main():
    last = time.time()
    while True:
        if time.time() - last >= 10:
            last = time.time()
            values_list_col1 = worksheet.col_values(1)
            values_list_col2 = worksheet.col_values(2)

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