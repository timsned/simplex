def eliminate(r1, r2, col, target=0):
    fac = (r2[col]-target) / r1[col]
    for i in range(len(r2)):
        r2[i] -= fac * r1[i]

def gauss(a):
    for i in range(len(a)):
        if a[i][i] == 0:
            for j in range(i+1, len(a)):
                if a[i][j] != 0:
                    a[i], a[j] = a[j], a[i]
                    break
            else:
                raise ValueError("Matrix is not invertible")
        for j in range(i+1, len(a)):
            eliminate(a[i], a[j], i)
    for i in range(len(a)-1, -1, -1):
        for j in range(i-1, -1, -1):
            eliminate(a[i], a[j], i)
    for i in range(len(a)):
        eliminate(a[i], a[i], i, target=1)
    return a

def inverse(a):
    tmp = [[] for _ in a]
    for i,row in enumerate(a):
        assert len(row) == len(a)
        tmp[i].extend(row + [0]*i + [1] + [0]*(len(a)-i-1))
    gauss(tmp)
    ret = []
    for i in range(len(tmp)):
        ret.append(tmp[i][len(tmp[i])//2:])
    return ret

################################################
#initial conditions


matrixa = [[0.08, 0.06, 1, 0, 0],
           [1, 0, 0, 1, 0],
           [0, 1, 0, 0, 1]]


b = [[12],
     [120],
     [120]]


c = [[-2],
     [-1.25],
     [0],
     [0],
     [0]]

starting_indexes = [2, 3, 4]

######################################################

def get_basis_size(matrix):
    num_rows = len(matrix)
    num_cols = len(matrix[0])
    basis_size = min([num_rows, num_cols])
    return basis_size


def get_basis(matrix, basis_size):
    basis_rows = matrix[-basis_size:]
    basis = []
    for row in basis_rows:
        basis.append(row[-basis_size:])
    return basis

def get_basis_from_columns(starting_indexes, matrix):
    basis = []
    for i in matrix:
        row = []
        for j in starting_indexes:
            print(j)
            row.append(i[j])
        basis.append(row)
    return basis

def get_xb(i_basis, b):
    result_vector = []
    for row in i_basis:
        counter = 0
        result_list = []
        for i in row:
            result = i*b[counter][0]
            result_list.append(result)
            counter += 1
        result_vector.append([sum(result_list)])
    return result_vector


def get_cost_basis(c_row, basis_indexes):
    cost_basis = []
    for i in basis_indexes:
        cost_basis.append(c_row[i])
    return cost_basis



def get_pi_transpose(cost_basis_vector, i_basis):
    result_vector = []
    for i in range(len(cost_basis_vector)):
        result_list = []
        for j in range(len(cost_basis_vector)):
            result_list.append(cost_basis_vector[j] * i_basis[j][i])
        result_vector.append(sum(result_list))
    return result_vector        




def get_pi_transpose_matrix(pi_transpose_vector, matrix):
    result_vector = []
    for i in range(len(matrix[0])):
        result_list = []
        for j in range(len(pi_transpose_vector)):
            result_list.append(pi_transpose_vector[j] * matrix[j][i])
        result_vector.append(sum(result_list))
    return result_vector   



def get_reduced_cost(c_row, pi_transpose_a):
    reduced_cost = []
    for i in range(len(c_row)):
        reduced_cost.append(c_row[i] - pi_transpose_a[i])
    return reduced_cost



def get_as(reduced_cost, matrix):
    min_index = reduced_cost.index(min(reduced_cost))
    vector = []
    for row in matrix:
        vector.append([row[min_index]])
    return vector



def get_basis_inverse_as(i_basis, as_vec):
    result_vector = []
    for row in i_basis:
        counter = 0
        result_list = []
        for i in row:
            result = i*as_vec[counter][0]
            result_list.append(result)
            counter += 1
        result_vector.append([sum(result_list)])
    return result_vector



def get_min_basis_index(xb, basis_inverse_as):
    result = []
    for i in range(len(xb)):
        if basis_inverse_as[i][0] > 0:
            result.append(xb[i][0]/basis_inverse_as[i][0])
    min_index = result.index(min(result))
    return min_index




###########################

def run(a, b, c, initial_column_indexes):
    basis_indexes = []
    c_row = [i[0] for i in c]
    basis_size = get_basis_size(a)
    basis_indexes = initial_column_indexes

    #basis = get_basis(a, basis_size)
    #basis_starting_col_index = len(a[0]) - basis_size
    #for i in range(basis_starting_col_index, len(a[0])):
    #    basis_indexes.append(i)
    basis = get_basis_from_columns(initial_column_indexes, a)
    running = True
    while running:
        inverse_basis = inverse(basis)
        xb = get_xb(inverse_basis, b)
        cost_basis_vector = get_cost_basis(c_row, basis_indexes)
        pi_transpose = get_pi_transpose(cost_basis_vector, inverse_basis)
        pi_transpose_matrix = get_pi_transpose_matrix(pi_transpose, a)
        reduced_cost = get_reduced_cost(c_row, pi_transpose_matrix)
        min_reduced_cost = min(reduced_cost)
        if min_reduced_cost > -0.0001:
            solution = []
            for i in range(len(a[0])):
                solution.append([0])
            for j in basis_indexes:
                solution[j] = xb[basis_indexes.index(j)]
                
            return solution
          
        as_vector = get_as(reduced_cost, a)
        basis_inverse_as = get_basis_inverse_as(inverse_basis, as_vector)
        min_basis_index = get_min_basis_index(xb, basis_inverse_as)
        column_to_add = []
        for i in a:
            column_to_add.append([i[reduced_cost.index(min_reduced_cost)]])
        for i in range(len(basis)):
            basis[i][min_basis_index] = column_to_add[i][0]
        #matrix_column_replaced = basis_indexes[min_basis_index]
        basis_indexes[min_basis_index] = reduced_cost.index(min_reduced_cost)





print(run(matrixa, b, c, starting_indexes))
