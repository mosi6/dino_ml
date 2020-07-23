import numpy as np
import random
class dino:
    def __init__(self,matrix1,matrix2):
        self.m1 = matrix1
        self.m2 = matrix2
    def step(self,in1,in2,in3):
        n = np.array([in1,in2,in3])
        n2 = np.dot(self.m1,n)
        n3 = np.dot(self.m2,n2)
        return int(n3)>0.5


def generate():
    r = random.uniform
    a = np.array([[r(-1,1),r(-1,1),r(-1,1)],[r(-1,1),r(-1,1),r(-1,1)],[r(-1,1),r(-1,1),r(-1,1)],[r(-1,1),r(-1,1),r(-1,1)]])
    b = np.array([r(-1,1),r(-1,1),r(-1,1),r(-1,1)])
    return [a,b]

def breed(dlst,a,b):
    p1 = dlst[a]
    p2 = dlst[b]
    childbody = []
    childhead = []
    for i in range(p1.m1.shape[0]):
        temp = []
        for j in range(p1.m1.shape[1]):
            r = random.random()
            if r<0.4:
                temp.append(p1.m1[i][j])
            elif r<0.8:
                temp.append(p2.m1[i][j])
            else:
                temp.append(random.uniform(-1,1))
        childbody.append(temp)
    for i in range(p1.m2.shape[0]):
        r = random.random()
        if r<0.45:
            childhead.append(p1.m2[i])
        elif r<0.9:
            childhead.append(p2.m2[i])
        else:
            childhead.append(random.uniform(-1,1))
    return dino(np.array(childbody),np.array(childhead))

    


def evolve(dlst,score,dinos):
    n=dinos
    total = sum([score[j]+0.1 for j in range(len(score))])
    probs = []
    parents = []
    nextgen=[]
    for j in score:
        probs.append((j+0.1)/total+sum(probs))
    for i in range(n):
        for s in range(2):
            choice = random.random()
            for u,num in enumerate(probs):
                if choice<num and num not in parents:
                    parents.append(u)
                    break
        nextgen.append(breed(dlst,parents[0],parents[1]))
    return nextgen

