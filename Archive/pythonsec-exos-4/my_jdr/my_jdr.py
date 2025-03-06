import random
from itertools import product

class AddExpr:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.result = 0
        self.results = []
        self.dice_count = 1
        self.op = self

    def throw(self) -> int:
        a = self.lhs.throw() if isinstance(self.lhs, AbstractResult) else self.lhs
        b = self.rhs.throw() if isinstance(self.rhs, AbstractResult) else self.rhs
        self.result = a + b
        self.results = [a, b]
        return self.result

    def show(self):
        return ', '.join(str(r) for r in self.results)

    def __add__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return AddExpr(self, rhs)

    def __mul__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return MulExpr(self, rhs)

    def __sub__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return SubExpr(self, rhs)

    def success(self, lamb):
        possible_results = []
        for outcome in product(*self.throws()):
            result = outcome[0] + outcome[1]
            if lamb(result):
                possible_results.append(outcome)
        return len(possible_results) / len(list(product(*self.throws())))

    def throws(self):
        if isinstance(self.lhs, AbstractResult):
            lhs_values = list(range(type(self.lhs).min, type(self.lhs).max + 1))
        else:
            lhs_values = [self.lhs]
        
        if isinstance(self.rhs, AbstractResult):
            rhs_values = list(range(type(self.rhs).min, type(self.rhs).max + 1))
        else:
            rhs_values = [self.rhs]
        
        return [lhs_values, rhs_values]

    def __radd__(self, lhs):
        if isinstance(lhs, int):
            return AddExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rmul__(self, lhs):
        if isinstance(lhs, int):
            return MulExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rsub__(self, lhs):
        if isinstance(lhs, int):
            return SubExpr(FrozenDice(lhs), self)
        return NotImplemented

class MulExpr:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.result = 0
        self.results = []
        self.dice_count = 1
        self.op = self

    def throw(self) -> int:
        a = self.lhs.throw() if isinstance(self.lhs, AbstractResult) else self.lhs
        b = self.rhs.throw() if isinstance(self.rhs, AbstractResult) else self.rhs
        self.result = a * b
        self.results = [a, b]
        return self.result

    def show(self):
        return ', '.join(str(r) for r in self.results)

    def __add__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return AddExpr(self, rhs)

    def __mul__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return MulExpr(self, rhs)

    def __sub__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return SubExpr(self, rhs)

    def success(self, lamb):
        possible_results = []
        for outcome in product(*self.throws()):
            result = outcome[0] * outcome[1]
            if lamb(result):
                possible_results.append(outcome)
        return len(possible_results) / len(list(product(*self.throws())))

    def throws(self):
        if isinstance(self.lhs, AbstractResult):
            lhs_values = list(range(type(self.lhs).min, type(self.lhs).max + 1))
        else:
            lhs_values = [self.lhs]
        
        if isinstance(self.rhs, AbstractResult):
            rhs_values = list(range(type(self.rhs).min, type(self.rhs).max + 1))
        else:
            rhs_values = [self.rhs]
        
        return [lhs_values, rhs_values]

    def __radd__(self, lhs):
        if isinstance(lhs, int):
            return AddExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rmul__(self, lhs):
        if isinstance(lhs, int):
            return MulExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rsub__(self, lhs):
        if isinstance(lhs, int):
            return SubExpr(FrozenDice(lhs), self)
        return NotImplemented

class SubExpr:
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs
        self.result = 0
        self.results = []
        self.dice_count = 1
        self.op = self

    def throw(self) -> int:
        a = self.lhs.throw() if isinstance(self.lhs, AbstractResult) else self.lhs
        b = self.rhs.throw() if isinstance(self.rhs, AbstractResult) else self.rhs
        self.result = a - b
        self.results = [a, b]
        return self.result

    def show(self):
        return ', '.join(str(r) for r in self.results)

    def __add__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return AddExpr(self, rhs)

    def __mul__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return MulExpr(self, rhs)

    def __sub__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return SubExpr(self, rhs)

    def success(self, lamb):
        possible_results = []
        for outcome in product(*self.throws()):
            result = outcome[0] - outcome[1]
            if lamb(result):
                possible_results.append(outcome)
        return len(possible_results) / len(list(product(*self.throws())))

    def throws(self):
        if isinstance(self.lhs, AbstractResult):
            lhs_values = list(range(type(self.lhs).min, type(self.lhs).max + 1))
        else:
            lhs_values = [self.lhs]
        
        if isinstance(self.rhs, AbstractResult):
            rhs_values = list(range(type(self.rhs).min, type(self.rhs).max + 1))
        else:
            rhs_values = [self.rhs]
        
        return [lhs_values, rhs_values]

    def __radd__(self, lhs):
        if isinstance(lhs, int):
            return AddExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rmul__(self, lhs):
        if isinstance(lhs, int):
            return MulExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rsub__(self, lhs):
        if isinstance(lhs, int):
            return SubExpr(FrozenDice(lhs), self)
        return NotImplemented

class AbstractResult:
    min = 1
    max = 1
    
    def __init__(self):
        self.result = 0
    
    def __repr__(self):
        return type(self).__name__

    def throw(self):
        if self.result == 0:
            self.result = random.randint(type(self).min, type(self).max)
        return self.result
    
    @staticmethod
    def seed(s):
        random.seed(s)

    def __add__(self, rhs):
        return AddExpr(self, rhs)
    
    def __mul__(self, rhs):
        return MulExpr(self, rhs)

    def __sub__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        return SubExpr(self, rhs)

    def __rsub__(self, lhs):
        if isinstance(lhs, int):
            return SubExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __radd__(self, lhs):
        if isinstance(lhs, int):
            return AddExpr(FrozenDice(lhs), self)
        return NotImplemented

    def __rmul__(self, lhs):
        if isinstance(lhs, int):
            return MulExpr(FrozenDice(lhs), self)
        return NotImplemented

class FrozenDice(AbstractResult):
    def __init__(self, v):
        self.result = v
        self.min = v
        self.max = v

    def __repr__(self):
        return str(self.result)

    def throw(self):
        return self.result

class D4(AbstractResult):
    max = 4

class D6(AbstractResult):
    max = 6

class D8(AbstractResult):
    max = 8

class D10(AbstractResult):
    max = 10

class D12(AbstractResult):
    max = 12

class D20(AbstractResult):
    max = 20

d4 = D4()
d6 = D6()
d8 = D8()
d10 = D10()
d12 = D12()
d20 = D20()

class Pool:
    def __init__(self, op, dice_count=1):
        self.op = op
        self.dice_count = dice_count
        self.results = []

    def throw(self):
        self.results = [self.op.throw() for _ in range(self.dice_count)]
        return sum(self.results)

    def roll(self):
        return self.throw()

    def show(self):
        return ', '.join(str(result) for result in self.results)

    def success(self, lamb):
        possible_results = []
        for outcome in product(*self.throws()):
            if lamb(sum(outcome)):
                possible_results.append(outcome)
        return len(possible_results) / len(list(product(*self.throws())))

    def throws(self):
        if isinstance(self.op, AbstractResult):
            values = list(range(type(self.op).min, type(self.op).max + 1))
            return [values] * self.dice_count
        return self.op.throws()

    def __add__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        if isinstance(rhs, AbstractResult):
            return Pool(AddExpr(self.op, rhs), self.dice_count)
        return NotImplemented

    def __mul__(self, rhs):
        if isinstance(rhs, int):
            return Pool(self.op, self.dice_count * rhs)
        if isinstance(rhs, AbstractResult):
            return Pool(MulExpr(self.op, rhs), self.dice_count)
        return NotImplemented

    def __sub__(self, rhs):
        if isinstance(rhs, int):
            rhs = FrozenDice(rhs)
        if isinstance(rhs, AbstractResult):
            return Pool(SubExpr(self.op, rhs), self.dice_count)
        return NotImplemented

    @staticmethod
    def darkness():
        return lambda x: sum(1 for i in x if i >= 5) >= 4
