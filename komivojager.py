import numpy as np
from python_tsp.exact import solve_tsp_dynamic_programming

distance_matrix = np.array([
    [0, 4, 5, 8, 13],
    [8, 0, 15, 15, 8],
    [18, 19, 0, 19, 13],
    [13, 2, 10, 0, 18],
    [15, 2, 11, 6, 0]
]
)

permutation, distance = solve_tsp_dynamic_programming(distance_matrix)
print("Built-in function")
print(permutation, distance)

inf = float('inf')
matrix = [
    [inf, 18,18,18, 13],
    [8, inf, 15, 15, 8],
    [18, 19, inf, 19, 13],
    [13, 2, 10, inf, 18],
    [15, 2, 11, 6, inf]
]




def min_row(a):
    minimum_row = []
    for i in range(len(a)):
        if all(value == float('-inf') for value in a[i]):
            minimum_row.append(0)
        else:
            minimum = min(a[i][j] for j in range(len(a[i])) if j != i and a[i][j] != float('-inf'))
            if minimum == inf:
                minimum = 0
            minimum_row.append(minimum)

    return minimum_row


def min_column(a):
    num_cols = len(a[0])
    minimum_column = []
    for j in range(num_cols):
        if all(row[j] == float('-inf') for row in a):
            minimum_column.append(0)
        else:
            min_val = min(row[j] for i, row in enumerate(a) if i != j and row[j] != float('-inf'))
            minimum_column.append(min_val)

    return minimum_column


def decrease_row(matrix, min_row):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i != j:
                matrix[i][j] -= min_row[i]
    return matrix


def decrease_column(matrix, min_column):
    for i in range(len(matrix)):
        for j in range(len(matrix[i])):
            if i != j:
                matrix[i][j] -= min_column[j]
    return matrix


def calculate_min_values(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])

    row_min_values = []
    col_min_values = []

    for i in range(num_rows):
        zeros_count = matrix[i].count(0)
        if zeros_count > 1:
            row_min_values.append(0)
        else:
            non_inf_values = [value for value in matrix[i] if value != float('-inf') and value != 0]
            if non_inf_values:
                min_val = min(non_inf_values)
                row_min_values.append(min_val)
            else:
                row_min_values.append(0)  # if all in row -inf

    for j in range(num_cols):
        col = [matrix[i][j] for i in range(num_rows)]
        zeros_count = col.count(0)
        if zeros_count > 1:
            col_min_values.append(0)
        else:
            non_inf_values = [value for value in col if value != float('-inf') and value != 0]
            if non_inf_values:
                min_val = min(non_inf_values)
                col_min_values.append(min_val)
            else:
                col_min_values.append(0)

    return row_min_values, col_min_values


def zero_counts(a):
    zero_results = []
    min_rows, min_cols = calculate_min_values(a)

    for i in range(len(a)):
        for j in range(len(a[i])):
            if a[i][j] == 0:
                min_sum = min_rows[i] + min_cols[j]
                zero_results.append(((i, j), a[i][j], min_sum))
    return zero_results


def include(a, i, j):
    new_matrix = [row[:] for row in a]

    new_matrix[j][i] = inf
    for k in range(len(new_matrix[i])):
        new_matrix[i][k] = float("-inf")
    for l in range(len(new_matrix)):
        new_matrix[l][j] = float("-inf")
    return new_matrix


def exclude(a, i, j):
    new_matrix = [row[:] for row in a]
    new_matrix[i][j] = inf
    return new_matrix


def check_matrix(matrix):
    for row in matrix:
        for value in row:
            if value not in (0, float('inf'), float('-inf')):
                return False
    return True

class Leaf:
    def __init__(self, matrix, path, length):
        self.matrix = matrix
        self.path = path
        self.length = length

minimum_rows = min_row(matrix)
decrease_row(matrix, minimum_rows)
minimum_columns = min_column(matrix)
decrease_column(matrix, minimum_columns)
h = sum(minimum_rows) + sum(minimum_columns)
path = []
leaves = [Leaf(matrix, path, h)]  # Починаємо з одного листка з початковою матрицею

while True:
    min_leaf = min(leaves, key=lambda x: x.length)
    matrix = min_leaf.matrix
    min_h = min_leaf.length
    path = min_leaf.path.copy()

    zeroes = zero_counts(matrix)
    max_value = float('-inf')
    max_idx = None
    for item in zeroes:
        if item[-1] > max_value:
            max_value = item[-1]
            max_idx = item[0]

    matrix_include = include(matrix, max_idx[0], max_idx[1])

    if check_matrix(matrix_include):
        path.append((max_idx[0], max_idx[1]))
        zeroes = zero_counts(matrix_include)
        for i in range(len(matrix_include)):
            for j in range(len(matrix_include[i])):
                if matrix[i][j] == 0:
                    if (i, j) in [x[0] for x in zeroes]:
                        idx = [x[0] for x in zeroes].index((i, j))
                        if zeroes[idx][2] == float('inf'):
                            path.append((i, j))
        break
    matrix_exclude = exclude(matrix, max_idx[0], max_idx[1])
    min_rows_include = min_row(matrix_include)
    decrease_row(matrix_include, min_rows_include)
    min_columns_include = min_column(matrix_include)
    decrease_column(matrix_include, min_columns_include)
    h_include = sum(min_rows_include) + sum(min_columns_include) + h

    min_rows_exclude = min_row(matrix_exclude)
    # decrease_row(matrix_exclude, min_rows_exclude)
    min_columns_exclude = min_column(matrix_exclude)
    # decrease_column(matrix_exclude, min_columns_exclude)
    h_exclude = sum(min_rows_exclude) + sum(min_columns_exclude) + h

    path_include = path.copy()
    path_include.append((max_idx[0], max_idx[1]))
    leaves.append(Leaf(matrix_include, path_include, h_include))

    path_exclude = path.copy()
    leaves.append(Leaf(matrix_exclude, path_exclude, h_exclude))

    leaves.remove(min_leaf)
# Calculate the final h value
final_h = 0
for i in range(len(path) ):
    final_h += distance_matrix[path[i][0]][path[i][1]]
# final_h += distance_matrix[path[-1][1]][path[0][0]]

print("My realization")
print(path)
print(final_h)

