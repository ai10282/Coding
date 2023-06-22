def insert_matrix(name=""):
    n, m = input(f"Enter size of {name}matrix: ").split()
    n = int(n)
    m = int(m)
    print(f"Enter {name}matrix:")
    return [[float(num) for num in input().split(' ')] for i in range(0, n)]


def add_matrices(matrix1, matrix2):
    if len(matrix1) == len(matrix2) and len(matrix1[0]) == len(matrix2[0]):
        result = [[matrix1[i][j] + matrix2[i][j] for j in range(len(matrix1[0]))] for i in range(len(matrix1))]
        print("The result is:")
        for f in result:
            print(*f)
    else:
        print("The operation cannot be performed.")


def multiply_by_constant(matrix, const):
    result = [[matrix[i][j] * const for j in range(len(matrix[0]))] for i in range(len(matrix))]
    print("The result is:")
    for f in result:
        print(*f)


def multiply(const, matrix):
    return [[matrix[i][j] * const for j in range(len(matrix[0]))] for i in range(len(matrix))]


def dot_product(list1, list2):
    return sum([list1[i] * list2[i] for i in range(len(list1))])


def transpose_matrix(matrix, t):
    if t == '1':
        return [[matrix[j][i] for j in range(len(matrix))] for i in range(len(matrix[0]))]
    elif t == '2':
        return [[matrix[j][i] for j in reversed(range(len(matrix)))] for i in reversed(range(len(matrix[0])))]
    elif t == '3':
        return [matrix[i][::-1] for i in range(len(matrix[0]))]
    elif t == '4':
        return [matrix[i] for i in reversed(range(len(matrix[0])))]
    else:
        print("There is no command like that!!!")
        return []


def multiply_matrices(matrix1, matrix2):
    if len(matrix1[0]) == len(matrix2):
        matrix2 = transpose_matrix(matrix2, '1')
        result = [[dot_product(matrix1[i], matrix2[j]) for j in range(len(matrix2))] for i in range(len(matrix1))]
        print("The result is:")
        for f in result:
            print(*f)
    else:
        print("The operation cannot be performed.")


def getMatrixMinor(m, i, j):
    return [row[:j] + row[j + 1:] for row in (m[:i] + m[i + 1:])]


def calculate_determinant(matrix):
    if len(matrix) == 1:
        return matrix[0][0]

    if len(matrix) == 2:
        return matrix[0][0] * matrix[1][1] - matrix[0][1] * matrix[1][0]

    determinant = 0
    for c in range(len(matrix)):
        determinant += ((-1) ** c) * matrix[0][c] * calculate_determinant(getMatrixMinor(matrix, 0, c))
    return determinant


def get_adj_matrix(matrix):
    return [[((-1) ** (i + j)) * calculate_determinant(getMatrixMinor(matrix, i, j)) for j in range(len(matrix[0]))] for
            i in
            range(len(matrix))]


def calculate_inverse(matrix):
    return multiply(1 / calculate_determinant(matrix), transpose_matrix(get_adj_matrix(matrix), "1"))


def show_menu():
    command = input("""1. Add matrices
2. Multiply matrix by a constant
3. Multiply matrices
4. Transpose matrix
5. Calculate a determinant
6. Inverse matrix
0. Exit
Your choice: """)

    if command == "0":
        return False
    elif command == "1":
        add_matrices(insert_matrix("first "), insert_matrix("second "))
        return True
    elif command == "2":
        multiply_by_constant(insert_matrix(), float(input("Enter constant: ")))
        return True
    elif command == "3":
        multiply_matrices(insert_matrix("first "), insert_matrix("second "))
        return True
    elif command == "4":
        choice = input("""1. Main diagonal
2. Side diagonal
3. Vertical line
4. Horizontal line
Your choice: """)
        result = transpose_matrix(insert_matrix(), choice)
        for f in result:
            print(*f)
    elif command == "5":
        print("The result is:\n")
        print(calculate_determinant(insert_matrix()))
    elif command == "6":
        matrix = insert_matrix()
        if calculate_determinant(matrix) == 0:
            print("This matrix doesn't have an inverse.")
        else:
            result = calculate_inverse(matrix)
            for f in result:
                print(*f)
    else:
        print("There is no like that command!!!")
        return True


while True:
    if not show_menu():
        break

