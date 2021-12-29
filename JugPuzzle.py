class Jug:
    def __init__(self,size):
        self.size = size
        self.amount = 0

    def empty(self):
        x = self.amount
        self.amount = 0
        return x

    def fill(self,amount = None):
        if amount is None:
            amount = self.size
        self.amount = amount
        return max(0, self.amount - amount)

class SetOfJugs:
    def __init__(self,jugs:list[Jug]) -> None:
        self.jugs = jugs

    def fill(self,index):
        self.jugs[index].fill()

    def empty(self,index):
        self.jugs[index].empty()

    def switch(self,index1,index2):
        x = self.jugs[index2].fill(self.jugs[index1].amount)
        self.jugs[index1].empty
        self.jugs[index1].fill(x)

    def __str__(self) -> str:
        s = [i.amount for i in self.jugs]
        return str(s)



Setj = SetOfJugs([Jug(9),Jug(5)])

print(Setj)