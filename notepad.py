myList=[[[0, 2], [-1, 3], [0, 6], [1, 3]], [[0, 2], [-1, 3], [0, 7], [1, 3]], [[0, 2], [-1, 3], [0, 8], [1, 3]], [[0, 2], [-1, 3], [0, 9], [1, 3]]]
newAsset1=[]


for i in range(0,len(myList)):
    for j in range(0,len(myList[i])):
        for k in range(0,len(myList[i][j])):
            myList[i][j][k]*=5.0
print(myList)