def dfs_tree(graph,start):
    visited=[]
    frontier=[]
    frontier.append(start)
    print(start)
    while len(frontier)>0:
        temp=frontier[0]
        li=graph[temp]
        j=0
        for i in li:
            if i not in visited:
                frontier.insert(0,i)
                print(i)
                break
            else:
                j=j+1
        if j==len(li):
            frontier.pop(0)
            
        visited.append(temp)




def main():
    graph={
    1:[4,3,2],
    2:[1,4,3],
    3:[1,2,4],
    4:[3,2,1]
    }
    dfs_tree(graph,1)


main()

