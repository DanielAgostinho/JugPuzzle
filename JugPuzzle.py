import matplotlib.pyplot as plt
 

class Jug:
    def __init__(self,size,amount = 0):
        self.size = size
        self.amount = amount

    def empty(self):
        x = self.amount
        self.amount = 0
        return x

    def fill(self):
        if self.amount == self.size:
            return False
        self.amount = self.size
        return True

    def set(self,amount):
        self.amount = amount


class SetOfJugs:
    def __init__(self,jugs:list[Jug]) -> None:
        self.jugs = jugs
 
    def switch(self,jug1:Jug,jug2:Jug):
        x1,y1 = jug1.amount, jug2.amount
        ylim =  jug2.size
        pos1 = [max(x1-ylim+y1,0),min(x1+y1,ylim)]
        jug1.amount, jug2.amount = pos1
        if pos1 == (x1,y1):
            return False
        return True

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
        
        if self.Jugs.amounts not in self.positions:
            self.positions.append(self.Jugs.amounts)
            return True
        return False

    def goal_reached(self,amounts):
        return self.goal in amounts

    def iteration(self,amounts):
        pos = []
        
        for i in self.Jugs.jugs:
            self.Jugs.set(amounts)
            valid = i.fill()
            if valid and self.Jugs.amounts not in self.positions:
                pos.append(self.Jugs.amounts)

            self.Jugs.set(amounts)
            valid = i.empty()
            if valid and self.Jugs.amounts not in self.positions:
                pos.append(self.Jugs.amounts)
            
            for j in self.Jugs.jugs:
                if i is not j:
                    self.Jugs.set(amounts)
                    valid = self.Jugs.switch(i,j)
                    if valid and self.Jugs.amounts not in self.positions:
                        pos.append(self.Jugs.amounts)

        self.Jugs.set(amounts)
        self.positions.extend(pos)
        return pos

    def solve(self):
        lines = []
        self.positions.append(self.Jugs.amounts)
        pos = self.iteration(self.Jugs.amounts)
        for p in pos:
            lines.append([self.Jugs.amounts,p])
        maxiter = (self.Jugs.jugs[0].size+1)*(self.Jugs.jugs[1].size+1)-(self.Jugs.jugs[0].size-1)*(self.Jugs.jugs[1].size-1)+1
        for _ in range(maxiter):
            pos1 = []
            for p in lines:
                x = p[-1]
                if not self.goal_reached(x):
                    response =self.iteration(x)
                    if len(response) == 1:
                        p.append(response[0])
                    else:
                        p = lines.pop(lines.index(p))
                        for r in response:
                            q = p[:]
                            q.append(r)
                            lines.append(q)                            

                    pos1.extend(response)
                    
            pos = pos1
            if not pos:
                break       
        return lines
        

Setj = SetOfJugs([Jug(9),Jug(5)])       
for n in range(1,max([i.size for i in Setj.jugs]) + 1):
    Setj.set([0]*len(Setj.jugs))
    Solve = Solver(Setj,n)
    solutions = Solve.solve()

    for line in solutions:
        x = [i[0] for i in line]
        y = [i[1] for i in line]
        plt.plot(x,y,'-*',label=len(line)-1)
        
    plt.legend(bbox_to_anchor=(0, 1, 1, 0), loc="lower left", ncol=min(len(solutions),5))
    plt.title(n)
    plt.show()