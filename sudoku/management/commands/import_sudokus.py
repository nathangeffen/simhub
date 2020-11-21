from django.core.management.base import BaseCommand, CommandError
from django.db import IntegrityError, transaction
from sudoku.models import Sudoku

class Command(BaseCommand):
    help = 'Load Sudoku puzzles from a file'

    def add_arguments(self, parser):
        parser.add_argument('file',  type=str)
        parser.add_argument('--difficulty', type=str, default='0')

    def handle(self, *args, **options):

        print(options['file'])
        print(options['difficulty'])


        with open(options['file']) as f:
            lines = f.readlines()
            try:
                with transaction.atomic():
                    for line in lines:
                        p = None
                        puzzle = line.split()[1]
                        if len(puzzle) != 81:
                            print("Puzzle length is incorrect", puzzle)
                            continue
                        for c in puzzle:
                            if c < '0' or c > '9':
                                print("Puzzle has invalid characters", puzzle)
                        try:
                            p = Sudoku.objects.get(puzzle=puzzle)
                            print("Puzzle exists (skipping):", p.pk, p.puzzle)
                        except Sudoku.DoesNotExist:
                            pass
                        if p is None:
                            s = Sudoku()
                            s.puzzle = puzzle
                            s.difficulty = options['difficulty']
                            s.save()
                            s.publish_now()
            except IntegrityError:
                print("Database integrity error. Transaction cancelled.")
