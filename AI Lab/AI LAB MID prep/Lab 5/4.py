def a_star(graph,hn,start):
    Open={start:hn[start]}
    closed=[]
    seq=[]
    curr=start
    while hn[curr] != 0:
        li=graph[curr]
        seq.append(curr)
        
        for i in li:
            Open[i[0]]=Open[curr]-hn[curr]+hn[i[0]]+i[1]
        
        Open.pop(curr)
        closed.append(curr)

        min_hn=list(Open.keys())[0]
        for i in Open.keys():
            if Open[i] < Open[min_hn]:
                min_hn=i
        
        curr=min_hn


    seq.append(curr)
    print("Sequence of nodes visited:",seq)
    res=path(seq,graph)
    print("Path of goal Node:",res[0])
    print("Cost of Path: ",res[1])


def path(seq,graph):
    i=len(seq)-1
    Path=[seq[i]]
    i=i-1
    sum=0
    while i>=0:
        li=graph[seq[i]]
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
    graph={
            "S":[("A",1),("G",10)],
            "A":[("C",1),("B",2)],
            "B":[("D",5)],
            "C":[("D",3),("G",4)],
            "D":[("G",4)],
            "G":[]
        }
    hn={
        "A":3,
        "B":4,
        "C":2,
        "D":6,
        "G":0,
        "S":5
    }
    a_star(graph,hn,"S")   

    

main()
