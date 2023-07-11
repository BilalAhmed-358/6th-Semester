def route(graph,start):
    arr=[start]
    cost=0
    not_visited=list(graph.keys())
    not_visited.remove(start)
    curr=start
    while not_visited:
        li=graph[curr]
        min_cost=99999
        for i in li:
            if i[0] in not_visited and min_cost > i[1]:
                min_cost=i[1]
                curr=i[0]
        not_visited.remove(curr)
        
        cost+=min_cost
        arr.append(curr)
    li=graph[curr]
    for i in li:
        if i[0]==start:
            cost+=i[1]
            break
    arr.append(start)
    print(arr)
    print(cost)

def main():
    graph={
    1:[(2,10),(3,15),(4,20)],
    2:[(1,10),(3,35),(4,25)],
    3:[(2,35),(1,15),(4,30)],
    4:[(1,20),(2,25),(3,30)]
            }
    route(graph,4)



main()
