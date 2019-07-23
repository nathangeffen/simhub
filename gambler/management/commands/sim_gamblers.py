#!python3

if __name__ != '__main__':
    from django.core.management.base import BaseCommand
import random
import sys


def simulate(startAmount, numTests, numGambles, numPlayers,
             outputFile=sys.stdout):
    total = 0
    wins = 0
    for _ in range(0, numTests):
        gamblers = [startAmount] * numPlayers
        broke = []
        casino = 0
        for i in range(0, numGambles):
            if len(gamblers):
                index = random.randint(0, len(gamblers) - 1)
                if random.random() < 0.5:
                    gamblers[index] += 1
                    casino -= 1
                else:
                    gamblers[index] -= 1
                    casino += 1
                if gamblers[index] == 0:
                    broke.append(i)
                    del gamblers[index:index+1]
            else:
                break
        print("Gamblers:", gamblers, "Broke:", broke, "Casino:", casino,
              file=outputFile)
        if casino > 0:
            wins += 1
        total += casino
    print("Casino total: ", total, "Casino wins: ", wins, file=outputFile)


if __name__ != '__main__':
    class Command(BaseCommand):
        help = 'Runs the gambling simulation'
        START_AMOUNT = 10
        NUM_TESTS = 5000
        NUM_GAMBLES = 100000
        NUM_PLAYERS = 10

        def add_arguments(self, parser):
            parser.add_argument('--amount', type=int, default=self.START_AMOUNT)
            parser.add_argument('--runs', type=int, default=self.NUM_TESTS)
            parser.add_argument('--gambles', type=int, default=self.NUM_GAMBLES)
            parser.add_argument('--players', type=int, default=self.NUM_PLAYERS)

        def handle(self, *args, **options):
            simulate(options['amount'], options['runs'],
                     options['gambles'], options['players'])


if __name__ == '__main__':
    import argparse
    START_AMOUNT = 10
    NUM_TESTS = 5000
    NUM_GAMBLES = 100000
    NUM_PLAYERS = 10

    parser = argparse.ArgumentParser(description='Run gambling simulation')

    parser.add_argument('--amount', type=int, default=START_AMOUNT)
    parser.add_argument('--runs', type=int, default=NUM_TESTS)
    parser.add_argument('--gambles', type=int, default=NUM_GAMBLES)
    parser.add_argument('--players', type=int, default=NUM_PLAYERS)
    parser.add_argument('--output', default=None)

    options = parser.parse_args()

    if options.output:
        output = open(options.output, "w")
    else:
        output = sys.stdout

    simulate(options.amount, options.runs, options.gambles, options.players,
             output)

    if options.output:
        output.close()
