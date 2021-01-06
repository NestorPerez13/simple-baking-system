class PiggyBank:
    # create __init__ and add_money methods
    def __init__(self, dollars, cents):
        self.dollars = 0
        self.cents = 0
        self.add_money(dollars, cents)

    def add_money(self, dollars, cents):
        self.cents += cents
        self.dollars += dollars
        if self.cents >= 100:
            self.dollars += self.cents // 100
            self.cents = self.cents % 100


piggy_bank = PiggyBank(1, 1)
# input_dollars, input_cents = map(int, input().split())
# piggy_bank.add_money(input_dollars, input_cents)
# print(piggy_bank.dollars, piggy_bank.cents)
