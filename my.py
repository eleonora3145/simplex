import numpy as np

class Problem:
    def __init__(self, c, A, b):
        self.c = np.append(c, [0.0 for _ in range(len(b))])  # Додаємо штучні змінні в цільову функцію
        self.A = np.hstack([A, np.eye(len(b))])  # Додаємо штучний базис до матриці обмежень
        self.b = b
        self.m, self.n = self.A.shape
        self.x = np.zeros(self.n)
        self.basic_index = list(range(self.n - self.m, self.n))  # Індекси базисних змінних

    def start_basis(self):
        self.B = self.A[:, self.basic_index]  # Початкова базисна матриця

    def get_reduced_costs(self):
        c_b = self.c[self.basic_index]
        B_inv = np.linalg.inv(self.B)
        p = np.dot(c_b, B_inv)
        return self.c - np.dot(p, self.A)

    def changeBasis(self, theta_min, theta_l_idx, j, u):
        l = self.basic_index[theta_l_idx]
        self.x[l] = 0
        self.x[j] = theta_min
        self.basic_index[theta_l_idx] = j
        self.B = self.A[:, self.basic_index]

    def get_cost(self):
        c_b = self.c[self.basic_index]
        B_inv = np.linalg.inv(self.B)
        x_b = np.dot(B_inv, self.b)
        return np.dot(c_b, x_b)


class SimplexMethod:
    def __init__(self, problem):
        self.problem = problem

    def run(self):
        self.problem.start_basis()
        reduced_costs = self.problem.get_reduced_costs()
        while any(reduced_costs < 0):
            j = np.argmin(reduced_costs)
            B_inv = np.linalg.inv(self.problem.B)
            u = np.dot(B_inv, self.problem.A[:, j])
            if all(u <= 0):
                print('Optimal X:\n{}'.format(self.problem.x))
                print('Optimal Z(cost): -inf')
                return
            theta = np.divide(self.problem.b, u, out=np.full_like(self.problem.b, np.inf), where=u > 0)
            theta_min = np.min(theta)
            theta_l_idx = np.argmin(theta)
            self.problem.changeBasis(theta_min, theta_l_idx, j, u)
            reduced_costs = self.problem.get_reduced_costs()
        print('Optimal X:\n{}'.format(self.problem.x))
        print('Optimal Z(cost): {}'.format(self.problem.get_cost()))


# Визначте коефіцієнти цільової функції
c = np.array([-2, 1])

# Визначте матрицю обмежень
A = np.array([[2, 1], [1, 1], [-3, 2]])

# Визначте вектор правих частин обмежень
b = np.array([8, 6, 3])

# Створіть об'єкт проблеми
problem = Problem(c, A, b)

# Створіть об'єкт симплекс-методу і запустіть його
simplex = SimplexMethod(problem)
simplex.run()
