import matplotlib.pyplot as plt
 

class Jug:
    def __init__(self,size,amount = 0):
        self.size = size
        self.amount = amount

    def empty(self):
        x = self.amount
        self.amount = 0
        return x

    def fill(self,amount = None):
        if amount is None:
            amount = self.size
        self.amount = min(amount + self.amount,self.size)
        
        return max(0,amount - self.amount)

    def set(self,amount):
        self.amount = amount


class SetOfJugs:
    def __init__(self,jugs:list[Jug]) -> None:
        self.jugs = jugs

    def fill(self,index):
        self.jugs[index].fill()

    def empty(self,index):
        self.jugs[index].empty()

    def switch(self,index1,index2):
        x1,y1 = self.jugs[index1].amount, self.jugs[index2].amount
        ylim =  self.jugs[index2].size
        pos1 = [max(x1-ylim+y1,0),min(x1+y1,ylim)]

        self.jugs[index1].amount, self.jugs[index2].amount = pos1

    def set(self,amounts:list):
        for jug,amount in zip(self.jugs,amounts):
            jug.set(amount)

    def __str__(self) -> str:
        s = [i.amount for i in self.jugs]
        return str(s)

    @property
    def amounts(self):
        return [i.amount for i in self.jugs]

class Solver:
    def __init__(self,Jugs:SetOfJugs,goal):
        self.positions = []
        self.Jugs = Jugs
        self.goal = goal

    def savepos(self):
        #if self.goal in self.Jugs.amounts:
        #    self.positions.append(self.Jugs.amounts)
        #    print(self.Jugs.amounts)
        #    return True
        if self.Jugs.amounts not in self.positions:
            self.positions.append(self.Jugs.amounts)
            return True
        return False

    def iteration(self,x,y,n=0):
        print(' '*n +'start of branch',x,y)

        self.Jugs.set([x,y])
        self.Jugs.switch(0,1)
        valid = self.savepos()
        if valid:
            print(' '*n +'Switch 0 1',self.Jugs.amounts)
            self.iteration(*self.Jugs.amounts)


        self.Jugs.set([x,y])
        self.Jugs.switch(1,0)
        valid = self.savepos()
        if valid:
            print(' '*n +'Switch 1 0',self.Jugs.amounts)
            self.iteration(*self.Jugs.amounts,n+1)

        for i in range(len(self.Jugs.jugs)):
            self.Jugs.set([x,y])
            self.Jugs.empty(i)
            valid = self.savepos()
            if valid:
                print(' '*n +'empty',i,self.Jugs.amounts)
                self.iteration(*self.Jugs.amounts,n+1)        

        for i in range(len(self.Jugs.jugs)):
            self.Jugs.set([x,y])
            self.Jugs.fill(i)
            valid = self.savepos()
            if valid:
                print(' '*n +'Fill ',i,self.Jugs.amounts)
                self.iteration(*self.Jugs.amounts,n+1)

        print(' '*n +'end of branch',self.Jugs.amounts)

        


    def solve(self):
        
        x,y = self.Jugs.amounts
        self.iteration(x,y)
        return self.positions

        

Setj = SetOfJugs([Jug(9),Jug(5)])
Solve = Solver(Setj,7)
print(Solve.solve())

line = []
for index in range(len(Solve.positions)-1):
    p1,p2 = (Solve.positions[index],Solve.positions[index+1])
    plt.plot([p1[0],p2[0]],[p1[1],p2[1]])
plt.show()

    