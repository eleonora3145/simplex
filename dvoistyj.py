import math

# Коефіцієнти цільової функції
coefficients = [-2, 1]
# Матриця обмежень
constraints = [[2, 1], [1, 1], [3, -2]]
# Вектор правих частин обмежень
bounds = [8, 6, -3]

# Функція для нормалізації рядка матриці обмежень
def normalize_row(constraints, row_index, column_index):
    pivot_element = constraints[row_index][column_index]
    constraints[row_index] = [element / pivot_element for element in constraints[row_index]]
    for i in range(len(constraints)):
        if i != row_index:
            factor = -1 * constraints[i][column_index]
            constraints[i] = [constraints[row_index][j] * factor + constraints[i][j] for j in range(len(constraints[i]))]
    return constraints

# Функція для визначення індексу головного стовпця
def find_pivot_column(constraints, pivot_row_idx):
    pivot_row = constraints[pivot_row_idx][:num_variables]
    last_row = constraints[-1][:num_variables]
    temp_array = []
    for i in range(len(pivot_row)):
        if pivot_row[i] < 0:
            temp_array.append(abs(last_row[i] / pivot_row[i]))
        else:
            temp_array.append(math.inf)
    pivot_column_idx = temp_array.index(min(temp_array))
    if min(temp_array) == math.inf:
        print("Cannot find the result")
        print('Z =', constraints[-1][-1])
        exit(1)
    return pivot_column_idx

# Функція для отримання стовпця матриці обмежень
def get_column(constraints, index):
    return [row[index] for row in constraints]

# Функція для визначення індексу головного рядка
def find_pivot_row(constraints, pivot_column_idx):
    pivot_column = get_column(constraints, pivot_column_idx)[:-1]
    last_column = get_column(constraints, len(constraints[0]) - 1)
    temp_array = []
    for i in range(len(pivot_column)):
        if pivot_column[i] != 0:
            if last_column[i] / pivot_column[i] >= 0:
                temp_array.append(last_column[i] / pivot_column[i])
            else:
                temp_array.append(math.inf)
        else:
            temp_array.append(math.inf)
    pivot_row_idx = temp_array.index(min(temp_array))
    if min(temp_array) == math.inf:
        print("Cannot find the result")
        print('Z = ', constraints[-1][-1])
        exit(1)
    return pivot_row_idx

# Чи максимізуємо ми цільову функцію?
maximize = True

size = len(bounds)
num_variables = len(constraints[0])

for i in range(size):
    for j in range(size):
        if i == j:
            constraints[i].append(1)
        else:
            constraints[i].append(0)

last_row = [i for i in coefficients]
for _ in range(len(bounds)):
    constraints[_].append(bounds[_])
    last_row.append(0)

last_row.append(0)

constraints.append(last_row)

index = num_variables

temp_vars = []
result_vars = []
for i in range(num_variables + len(bounds)):
    temp_vars.append('X' + str(i + 1))
    if i >= num_variables:
        result_vars.append('X' + str(i + 1))

condition = True
while condition:
    last_column = get_column(constraints, len(constraints[0]) - 1)[:-1]
    if maximize:
        if min(last_column) < 0:
            pivot_row_idx = last_column.index(min(last_column))
            pivot_column_idx = find_pivot_column(constraints, pivot_row_idx)
        else:
            last_row = constraints[-1][:-1]
            if min(last_row) < 0:
                pivot_column_idx = last_row.index(min(last_row))
                pivot_row_idx = find_pivot_row(constraints, pivot_column_idx)
            else:
                break
    else:
        if min(last_column) < 0:
            pivot_row_idx = last_column.index(min(last_column))
            pivot_column_idx = find_pivot_column(constraints, pivot_row_idx)
        else:
            last_row = constraints[-1][:-1]
            if max(last_row) > 0:
                pivot_column_idx = last_row.index(max(last_row))
                pivot_row_idx = find_pivot_row(constraints, pivot_column_idx)
            else:
                break
    result_vars[pivot_row_idx] = temp_vars[pivot_column_idx]
    normalize_row(constraints, pivot_row_idx, pivot_column_idx)

result_vars.append('Z')
print("Solution:")
for i in range(len(constraints)):
    if result_vars[i] == 'X2' or result_vars[i] == 'X1':
        print(constraints[i][-1], end=' ')
print("\nObjective function value: ", constraints[-1][-1])