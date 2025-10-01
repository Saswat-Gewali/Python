# 3x3 matrix
X = [[12, 7, 3],
     [4, 5, 6],
     [7, 8, 9]]

# 3x4 matrix
Y = [[5, 8, 1, 2],
     [6, 7, 3, 0],
     [4, 5, 9, 1]]

# result is 3x4 matrix
result = [[0, 0, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 0]]

# Nested loops to perform matrix multiplication
for i in range(len(X)):              # iterate over rows of X
    for j in range(len(Y[0])):       # iterate over columns of Y
        for k in range(len(Y)):      # iterate over rows of Y (same as columns of X)
            result[i][j] += X[i][k] * Y[k][j]

# Print the result
for r in result:
    print(r)
