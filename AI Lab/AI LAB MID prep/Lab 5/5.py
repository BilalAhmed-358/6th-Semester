def greedy(maze,start,row,col):
    Open=[start]
    closed=[]
    seq=[]
    curr=start
    while maze[curr[0]][curr[1]] != 0:
        seq.append(curr)
        
        if curr[0]-1 >= 0 and maze[curr[0]-1][curr[1]]!=-1 :
            if (curr[0]-1,curr[1]) not in seq:
                Open.append((curr[0]-1,curr[1]))
        if curr[0]+1 <= row-1 and maze[curr[0]+1][curr[1]] !=-1:
            if (curr[0]+1,curr[1]) not in seq:
                Open.append((curr[0]+1,curr[1]))
        if curr[1]-1 >= 0 and maze[curr[0]][curr[1]-1]!=-1:
            if (curr[0],curr[1]-1) not in seq:
                Open.append((curr[0],curr[1]-1))
        if curr[1]+1 <= col-1 and maze[curr[0]][curr[1]+1] !=-1:
            if (curr[0],curr[1]+1) not in seq:
                Open.append((curr[0],curr[1]+1))
        
        Open.remove(curr)
        closed.append(curr)
        min_hn=Open[0]
        for i in Open:
            if maze[min_hn[0]][min_hn[1]] > maze[i[0]][i[1]]:
                min_hn=i
        
        curr=min_hn


    seq.append(curr)
    print("Sequence of nodes visited:\n",seq)
    res=path(seq,maze)
    print("Path of goal Node:\n",res[0])
    print("Total Cost of Path: ",res[1])

def a_star(maze,start,row,col):
    start1=(start[0],start[1],0)
    Open=[start1]
    closed=[]
    seq=[]
    curr=start1
    while maze[curr[0]][curr[1]] != 0:
        seq.append((curr[0],curr[1]))
        if curr[0]-1 >= 0 and maze[curr[0]-1][curr[1]]!=-1 :
            if (curr[0]-1,curr[1]) not in seq:
                Open.append((curr[0]-1,curr[1],curr[2]+1+maze[curr[0]-1][curr[1]]))
        if curr[0]+1 <= row-1 and maze[curr[0]+1][curr[1]] !=-1:
            if (curr[0]+1,curr[1]) not in seq:
                Open.append((curr[0]+1,curr[1],curr[2]+1+maze[curr[0]+1][curr[1]]))
        if curr[1]-1 >= 0 and maze[curr[0]][curr[1]-1]!=-1:
            if (curr[0],curr[1]-1) not in seq:
                Open.append((curr[0],curr[1]-1,curr[2]+1+maze[curr[0]][curr[1]-1]))
        if curr[1]+1 <= col-1 and maze[curr[0]][curr[1]+1] !=-1:
            if (curr[0],curr[1]+1) not in seq:
                Open.append((curr[0],curr[1]+1,curr[2]+1+maze[curr[0]][curr[1]+1]))
        
        Open.remove(curr)
        closed.append(curr)
        min_hn=Open[0]
        for i in Open:
            if min_hn[2] > i[2]:
                min_hn=i
        
        curr=min_hn


    seq.append((curr[0],curr[1]))
    print("Sequence of nodes visited:\n",seq)
    res=path(seq,maze)
    print("Path of goal Node:\n",res[0])
    print("Total Cost of Path: ",res[1])



def path(seq,maze):
    i=len(seq)-1
    Path=[seq[i]]
    sum=0
    curr=seq[i]
    i=i-1
    while i>=0:
        
        if abs(seq[i][0]-curr[0])+abs(seq[i][1]-curr[1])==1:
            sum+=1
            Path.insert(0,seq[i])
            curr=seq[i]

        i=i-1
    return (Path,sum)




def main():
    maze=[
            [-1 ,10 ,9  ,8  ,7  ,6  ,5  ,4  ,3  ,2  ,1  ,0 ],
            [-1 ,11 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,-1 ,1 ],
            [-1 ,12 ,-1 ,10 ,9  ,8  ,7  ,6  ,5  ,4  ,-1 ,2 ],
            [-1 ,13 ,-1 ,11 ,-1 ,-1 ,-1 ,-1 ,-1 ,5  ,-1 ,3 ],
            [-1 ,14 ,13 ,12 ,-1 ,10 ,9  ,8  ,7  ,6  ,-1 ,4 ],
            [-1 ,-1 ,-1 ,13 ,-1 ,11 ,-1 ,-1 ,-1 ,-1 ,-1 ,5 ],
            ['S'  ,16 ,15 ,14 ,-1 ,12 ,11 ,10 ,9  ,8  ,7  ,6 ],
            ]
    print("Greedy best first")
    greedy(maze,(6,0),len(maze),len(maze[0]))   
    print("A* search")
    a_star(maze,(6,0),len(maze),len(maze[0]))
    

main()
