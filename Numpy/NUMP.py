#1
import numpy as np

arr = np.array([])

print(arr)





#2
import numpy as np

salary=np.array([
25000,
35000,
40000,
50000
])

print("Type =",type(salary))
print("Shape =",salary.shape)
print("Dimensions =",salary.ndim)
print("Size =",salary.size)
print("Datatype =",salary.dtype)




#3
import numpy as np

a=np.array([1,2,3])

b=np.zeros(5)

c=np.ones(5)

d=np.empty(5)

e=np.eye(3)

f=np.identity(3)

g=np.arange(0,10,2)

h=np.linspace(0,1,5)

i=np.full((2,2),7)




#4
import numpy as np

arr = np.array([10,20,30,40,50])

# View
v = arr.view()

# Copy
c = arr.copy()

# Fancy Indexing
print(arr[[0,2,4]])

# Boolean Indexing
print(arr[arr>25])

# np.where()
print(np.where(arr>30,"Big","Small"))




#5
import numpy as np

a = np.array([10,20,30])
b = np.array([1,2,3])

print(a+b)
print(a*2)

arr = np.array([[1,2,3],
                [4,5,6]])

print(arr+10)

c = np.array([[1],[2],[3]])
d = np.array([10,20,30])

print(c+d)




#6
import numpy as np

a = np.array([10,20,30])
b = np.array([1,2,3])

print(np.add(a,b))
print(np.subtract(a,b))
print(np.multiply(a,b))
print(np.divide(a,b))
print(np.power(a,2))
print(np.sqrt(a))
print(np.square(a))
print(np.abs(np.array([-5,5])))





#7
import numpy as np

arr = np.array([10,20,30,40,50])

print(np.sum(arr))
print(np.mean(arr))
print(np.median(arr))
print(np.min(arr))
print(np.max(arr))
print(np.argmin(arr))
print(np.argmax(arr))
print(np.std(arr))
print(np.var(arr))



#8
import numpy as np

arr = np.array([1,2,3,4,5,6])

print(arr.reshape(2,3))
print(arr.reshape(3,-1))
print(arr.reshape(-1,1))

matrix = np.array([[1,2],[3,4]])

print(matrix.flatten())
print(matrix.ravel())
print(matrix.T)

a = np.array([1,2,3])
print(np.expand_dims(a, axis=0))
print(np.expand_dims(a, axis=1))

b = np.array([[1,2,3]])
print(np.squeeze(b))





#9
import numpy as np

a=np.array([1,2,3])
b=np.array([4,5,6])

print(np.concatenate((a,b)))
print(np.vstack((a,b)))
print(np.hstack((a,b)))
print(np.stack((a,b)))

arr=np.array([10,20,30,40])

print(np.split(arr,2))

print(np.random.rand(3))
print(np.random.randn(3))
print(np.random.randint(1,10,5))

colors=np.array(["Red","Blue","Green"])
print(np.random.choice(colors))

np.random.shuffle(arr)
print(arr)

np.random.seed(10)
print(np.random.randint(1,100,5))