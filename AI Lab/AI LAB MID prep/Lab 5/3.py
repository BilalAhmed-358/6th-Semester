def greedy(tree,hn,start):
    Open=[start]
    closed=[]
    seq=[]
    curr=start
    while hn[curr] != 0:
        li=tree[curr]
        seq.append(curr)
        
        for i in li:
            if i[0] not in Open:
                Open.append(i[0])
        Open.remove(curr)
        closed.append(curr)

        min_hn=Open[0]
        for i in Open:
            if hn[min_hn] > hn[i]:
                min_hn=i
        
        curr=min_hn


    seq.append(curr)
    print("Sequence of nodes visited:",seq)
    res=path(seq,tree)
    print("Path of goal Node:",res[0])
    print("Cost of Path: ",res[1])


def path(seq,tree):
    i=len(seq)-1
    Path=[seq[i]]
    i=i-1
    sum=0
    while i>=0:
        li=tree[seq[i]]
        flag=False
        for temp in li:
            if temp[0]==Path[0]:
                flag=True
                sum+=temp[1]
                break
        if flag:
            Path.insert(0,seq[i])
        i=i-1
    return (Path,sum)




def main():
    tree={
            "S":[("A",3),("B",2)],
            "A":[("C",4),("D",1)],
            "B":[("E",3),("F",1)],
            "C":[],
            "D":[],
            "E":[("H",5)],
            "F":[("I",2),("G",3)],
            "G":[],
            "H":[],
            "I":[]
        }
    hn={
        "A":12,
        "B":4,
        "C":7,
        "D":3,
        "E":8,
        "F":2,
        "G":0,
        "H":4,
        "I":9,
        "S":13
    }
    greedy(tree,hn,"S")   

    

main()
