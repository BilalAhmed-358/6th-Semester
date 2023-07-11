import time
res=[[1,2,3],[4,5,6],[7,8,0]]

def check(arr):
    j=0
    i=0
    while i<3:
        j=0
        while j<3:
            if arr[i][j]!=res[i][j]:
                return False
            j+=1
        i+=1
    return True

def checktwo(arr1,arr2):
    j=0
    i=0
    while i<3:
        j=0
        while j<3:
            if arr1[i][j]!=arr2[i][j]:
                return False
            j+=1
        i+=1
    return True

def findzero(arr):
    i,j=0,0
    while i<3:
        j=0
        while j<3:
            if arr[i][j]==0:
                return (i,j)
            j=j+1
        i=i+1
def newarr(arr):
    temp=[]
    temp1=[]
    for i in arr:
        temp1=[]
        for j in i:
            temp1.append(j)
        temp.append(temp1)

    return temp
def bfs(arr):
    queue=[]
    queue.append((arr,newarr(arr)))
    prev=[]
    while len(queue)>0:
        
        temp=queue.pop(0)
        print(temp[0])
        #time.sleep(3)
        prev=temp[1]
        temp=temp[0]
        j=findzero(temp)
        i=j[0]
        j=j[1]
        if i-1 >= 0:
            temp1=newarr(temp)
            temp1[i][j],temp1[i-1][j]=temp1[i-1][j],temp1[i][j]
            if not checktwo(temp1,prev):
                if check(temp1):
                    return temp1
                queue.append((temp1,temp))
            
        if j-1 >=0:
            temp1=newarr(temp)
            temp1[i][j],temp1[i][j-1]=temp1[i][j-1],temp1[i][j]
            if not checktwo(temp1,prev):
                if check(temp1):
                    return temp1 
                queue.append((temp1,prev))
        if j+1 <=2:
            temp1=newarr(temp)
            temp1[i][j],temp1[i][j+1]=temp1[i][j+1],temp1[i][j]
            if not checktwo(temp1,prev):
                if check(temp1):
                    return temp1
                queue.append((temp1,prev))
        if i+1 <=2:
            temp1=newarr(temp)
            temp1[i][j],temp1[i+1][j]=temp1[i+1][j],temp1[i][j]
            if not checktwo(temp1,prev):
                if check(temp1):
                    return temp1
                queue.append((temp1,prev))
        
        
def dfs(arr,arr1,z):
        z=z+1
        if z==25:
            return None
        print(arr)
        j=findzero(arr)
        i=j[0]
        j=j[1]
        if i-1 >= 0:
            temp1=newarr(arr)
            temp1[i][j],temp1[i-1][j]=temp1[i-1][j],temp1[i][j]
            if not checktwo(temp1,arr1):
                if check(temp1):
                    return temp1

                res=dfs(temp1,arr,z)
                if res is not None:
                    return res
        if j-1 >=0:
            temp1=newarr(arr)
            temp1[i][j],temp1[i][j-1]=temp1[i][j-1],temp1[i][j]
            if not checktwo(temp1,arr1):
                if check(temp1):
                    return temp1 

                res= dfs(temp1,arr,z)
                if res is not None:
                    return res
        if j+1 <=2:
            temp1=newarr(arr)
            temp1[i][j],temp1[i][j+1]=temp1[i][j+1],temp1[i][j]
            if not checktwo(temp1,arr1):
                if check(temp1):
                    return temp1
                res= dfs(temp1,arr,z)
                if res is not None:
                    return res
        if i+1 <=2:
            temp1=newarr(arr)
            temp1[i][j],temp1[i+1][j]=temp1[i+1][j],temp1[i][j]
            if not checktwo(temp1,arr1):
                if check(temp1):
                    return temp1

                res= dfs(temp1,arr,z) 
                if res is not None:
                    return res
     

    
def main():
    arr=[[7,8,6],[1,2,3],[5,4,0]]
    if check(arr):
        print(arr)
        return
    print(dfs(arr,newarr(arr),0))
     

main()
