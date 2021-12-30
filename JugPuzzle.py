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

class Node:
    def __init__(self,value,parent = None):
        self.value = value
        self.parent = parent
        if self.parent is not None:
            self.parent.add(self)
        self.childs:list[Node] = []

    def get_chain(self):
        
        print(f'{self.parent.value if self.parent is not None else ""}->{self.value} -> {[i.value for i in self.childs]}')
        for i in self.childs:
            i.get_chain()
    
    def plot_chain(self):
        v1 = self.value
        for i in self.childs:
            v2 = i.value
            if not (v1[0] != v2[0] and v1[1] != v2[1] and abs((v1[1] - v2[1])/(v1[0] - v2[0])) != 1):

                plt.plot([v1[0],v2[0]],[v1[1],v2[1]])
            i.plot_chain()

    def add(self,node):
        self.childs.append(node)

    def __dict__(self):
        return {str(self.value):[i.__dict__() for i in self.childs]}

    def l(self):
        return self.value,[i.l() for i in self.childs]
    



class Solver:
    def __init__(self,Jugs:SetOfJugs,goal):
        self.node = Node([0,0])
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
            lines.append((self.Jugs.amounts,p))
        print(pos)
        for _ in range(20):
            pos1 = []
            for p in pos:
                if not self.goal_reached(p):
                    response =self.iteration(p)
                    for r in response:
                        lines.append((p,r))
                    pos1.extend(response)
            pos = pos1
            if not pos:
                break
            print(pos)
        print(len(self.positions))
        return lines
        

        

Setj = SetOfJugs([Jug(9),Jug(5)])
Solve = Solver(Setj,7)
solutions = Solve.solve()

for sol in solutions:
    plt.plot((sol[0][0],sol[1][0]),(sol[0][1],sol[1][1]))
plt.show()





#results = Solve.node.l()

#print(results)

