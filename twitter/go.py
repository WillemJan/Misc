#!/usr/bin/env python
 
from pprint import pprint

class solve_puzzle(object):
    tree=[]


    def __init__(self):
        f=open("triangle.txt", "r")
        data=f.read()
        f.close()
        for line in data.split('\n'):
            line=line.replace('\r','')
            if line: 
                self.tree.append(line.split(" "))

    def solve(self):

        curr=self.tree.pop()
        next=self.tree.pop()
        new=[]
        for i in range(0,len(next)):
            new.append(max(int(next[i])+int(curr[i]), int(next[i])+int(curr[i+1])))

        curr=self.tree.pop()
        next=self.tree.pop()
        for i in range(0,len(curr)):
            print(max(int(curr[i])+int(new[i]), int(curr[i])+int(new[i+1])))
            

if __name__ == "__main__":
    s=solve_puzzle()
    s.solve()

