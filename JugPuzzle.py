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

    def iteration(self,x,y,node,n=0):
        #print(' '*n +'start of branch',x,y)
        NNode = Node([x,y],node)
        if self.goal_reached([x,y]):
            return
        for i in range(len(self.Jugs.jugs)):
            self.Jugs.set([x,y])
            self.Jugs.fill(i)
            valid = self.savepos()
            if valid:
                #print(' '*n +'Fill ',i,self.Jugs.amounts)
                self.iteration(*self.Jugs.amounts,NNode,n+1)


            for k in range(len(self.Jugs.jugs)):
                if i != k:
                    self.Jugs.set([x,y])
                    self.Jugs.switch(i,k)
                    valid = self.savepos()
                    if self.Jugs.amounts == [0,0]:
                        valid = False
                    if valid:
                        #print(' '*n +'Switch',i,k,self.Jugs.amounts)
                        self.iteration(*self.Jugs.amounts,NNode,n+1)

            self.Jugs.set([x,y])
            self.Jugs.empty(i)
            valid = self.savepos()
            if valid:
                #print(' '*n +'empty',i,self.Jugs.amounts)
                self.iteration(*self.Jugs.amounts,NNode,n+1)        

        
            

        Node(self.Jugs.amounts,node)
        #print(' '*n +'end of branch',self.Jugs.amounts)

    def optimize(self):
        for i in range(len(self.positions)-3):
            pos1 = self.positions[i]
            pos2 = self.positions[i+1]
            pos3 = self.positions[i+2]
            if pos1[1] == pos2[1] == pos3[1]:
                self.positions.pop(i+1)

    def solve(self):
        x,y = self.Jugs.amounts
        self.iteration(x,y,self.node)
        #self.optimize()
        return self.positions

        

Setj = SetOfJugs([Jug(9),Jug(5)])
Solve = Solver(Setj,7)
Solve.solve()

#Solve.node.get_chain()

#for index in range(len(Solve.positions)-1):
#    p1,p2 = (Solve.positions[index],Solve.positions[index+1])
#    plt.plot([p1[0],p2[0]],[p1[1],p2[1]])

Solve.node.plot_chain()
plt.show()





results = Solve.node.l()

print(results)

