import matplotlib.pyplot as plt
import tkinter as tk
from math import ceil
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


class Gui:
    def __init__(self):
        bgcolor = '#73A2FF'
        self.ws = tk.Tk()
        self.ws.title('PythonGuides')
        self.ws.geometry('300x200')
        self.ws.config(bg=bgcolor)
        
        self.frame = tk.Frame(self.ws,bg=bgcolor)

        tk.Label(self.frame, text="Jug 1",bg=bgcolor).grid(row=0, column=0)
        tk.Label(self.frame, text="Jug 2",bg=bgcolor).grid(row=0, column=1)
        

        self.jug1 = tk.Entry(self.frame)
        self.jug1.grid(row=1, column=0)
        self.jug2 = tk.Entry(self.frame)
        self.jug2.grid(row=1, column=1)

        tk.Label(self.frame, text="Goal: ",bg=bgcolor).grid(row=2, column=0)
        self.goal = tk.Entry(self.frame)
        self.goal.grid(row=2, column=1)
        
        self.errorLabel = tk.Label(self.frame, text="",fg='#FF0000',bg=bgcolor)
        self.errorLabel.grid(row=4, column=1,columnspan=2)
        tk.Button(self.frame, text="Solve",command=self.solve).grid(row=3, columnspan=2, sticky='ew')

        
        self.frame.pack(expand=True) 
        self.ws.mainloop()

    def solve(self):
        self.errorLabel.config(text="")
        jug1 = self.jug1.get()
        jug2 = self.jug2.get()
        goal = self.goal.get()
        if not jug1.isnumeric() and not jug2.isnumeric():
            
            self.errorLabel.config(text='jug1 and jug2 are not valid')
        elif not jug1.isnumeric() or float(jug1) <= 0:
            self.errorLabel.config(text="jug1 is not valid")
        elif not jug2.isnumeric() or float(jug2) <= 0:
            self.errorLabel.config(text="jug1 is not valid")
        else:
            self.errorLabel.config(text=" ")
            if len(goal) == 0 or (goal.isnumeric() and float(goal) > 0 and float(goal) <= max(float(jug1),float(jug2))):
                if goal == '':
                    main(int(jug1),int(jug2))
                else:
                    main(int(jug1),int(jug2),int(goal))
            else:
                self.errorLabel.config(text="Goal is not valid")

def main(a,b,m=False):
    Setj = SetOfJugs([Jug(a),Jug(b)])       
    for n in range(1,int(ceil(max([i.size for i in Setj.jugs]) + 1))):
        if m is not False and n != m:
            continue
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

Gui()