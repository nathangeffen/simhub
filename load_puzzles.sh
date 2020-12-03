#!/bin/sh
source ~/workspace/django3/bin/activate
python3 ./manage.py  import_sudokus puzzles_f1.txt --start_date 20201130050000
python3 ./manage.py  import_sudokus puzzles_f2.txt --start_date 20201201050000
python3 ./manage.py  import_sudokus puzzles_f3.txt --start_date 20201202050000
python3 ./manage.py  import_sudokus puzzles_f4.txt --start_date 20201203050000
python3 ./manage.py  import_sudokus puzzles_f5.txt --start_date 20201204050000
python3 ./manage.py  import_sudokus puzzles_f6.txt --start_date 20201205050000
python3 ./manage.py  import_sudokus puzzles_f7.txt --start_date 20201206050000
