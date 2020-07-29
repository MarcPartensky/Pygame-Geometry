import numpy as np
A = np.array([[4, 0], [4, -3]])
B = np.array([[6, 2], [10, 2]])
t, s = np.linalg.solve(np.array([A[1]-A[0], B[0]-B[1]]).T, B[0]-A[0])

print(a,b)
c=np.linalg.solve(a,b)
print(c)
