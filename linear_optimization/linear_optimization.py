__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


import numpy as np
from typing import Optional

# a function to initialize a numpy array
def initialize_array(num_decision_variables: int, num_constraints: int, objectives: list, lhs_coef: list[list[int]], rhd_coef:list[int]) -> tuple[np.ndarray, int, int]:
    """
    Initialize a table for the tabular simplex. This table has dimensionality of (num_all_variables-2)*(num_all_variables+1).
    It also returns the coefficients of the objective function, including the slack variable.
    :param num_decision_variables: number of decision variables
    :param num_constraints: number of constraints (excluding x,y >= 0)
    :param objectives: coefficients of decision variables in the objective function
    :param lhs_coef: the coefficients of equations on the left hand side
    :param rhd_coef: the value on the right hand side
    :return: table, coefficients of the objective function, number of decision variables
    """
    objective_coefs = np.array(objectives + [0] * num_constraints)
    table = np.zeros((num_constraints, num_decision_variables + num_constraints+1))  # +1 for RHS
    # index_map: list[int] = [x for x in range(len(num_decision_variables))]  # each index implies a row index in the table; the element represents the index of the original location

    table[:, :num_decision_variables] = np.array(lhs_coef)

    # initialize LHS
    row_indices_to_make_1 = np.arange(len(table))
    column_indices_to_make_1 = np.arange(num_decision_variables, table.shape[1]-1)
    table[row_indices_to_make_1, column_indices_to_make_1] = 1

    # initialize RHS
    table[:, table.shape[1]-1] = rhd_coef

    return table, objective_coefs, num_decision_variables


def tabular_simplex(table: np.ndarray, objective_coefs: np.ndarray, num_decision_variables: int, e=0.001):
    """
    Compute the maximum value of the given objective function.
    Assumes that there is always one unique solution to the objective function. (no infinitely many/no solutions)
    :param table: the main table to work with.
    :param objective_coefs: coefficients of objective function. This includes the coefficients of slack variables too.
    :param num_decision_variables: number of decision variables in the objective function
    :param e: the error tolerance parameter - we need this because we are comparing float to integer
    :return: decision_variable_coefficients and maximized objective function value
    """
    decision_variable_index_map: list[Optional[tuple[int, int]]] = []  # decision_variable_idx, nth_row in the table

    while True:
        # solve z in terms of the basic variables -> dot product
        # choose basic varaible that will increase z more
        non_basic_coefs = np.zeros(len(table))

        for decision_variable_id, nth_row in decision_variable_index_map:
            non_basic_coefs[nth_row] = objective_coefs[decision_variable_id]


        z_coefs = objective_coefs - table[:, :-1].T @ non_basic_coefs  # c_j - Z_j
        leaving_basic_variable = np.argmax(z_coefs)

        if z_coefs[leaving_basic_variable] <= e:
            # no more feasible updates -> exit
            # calculate z
            current_decision_variable_values = np.zeros(len(objective_coefs))

            # for any decision variables that's not basic -> they are non-basic -> just get the RHS value
            for decision_variable_id, nth_row in decision_variable_index_map:
                current_decision_variable_values[decision_variable_id] = table[nth_row, -1]

            optimal_objective = current_decision_variable_values @ objective_coefs
            return current_decision_variable_values[:num_decision_variables], optimal_objective

        # for each row calculate the theta value i.e. the selected basic vaariable -> do argmin
        with np.errstate(divide='ignore'):
            theta = table[:, -1] / table[:, leaving_basic_variable]
        th_min = np.min(theta[theta>0])
        pivot_row = np.where(theta == th_min)[0][0]



        pivot_col = leaving_basic_variable
        pivot_elem = table[pivot_row, pivot_col]

        # do preprocessing for next iteration
        # divide by the row by the pivot element
        table[pivot_row] = table[pivot_row] / pivot_elem
        decision_variable_index_map.append((pivot_col, pivot_row))

        # do row operations to make the pivot column all 0, except for the pivot element
        # find the gap in the pivot elemnent
        for i in range(len(table)):
            # except for the pivot row AND if the element is 0 already you don't need to do anything
            if i != pivot_row and not -e <= table[i, pivot_col] <= e:
                # table[i] = table[new_basic_variable, leaving_basic_variable] \
                #            - table[i] / (table[new_basic_variable, leaving_basic_variable]/table[i, leaving_basic_variable])

                # table[i] = table[i] * (1/table[i, pivot_col]) - table[pivot_row]
                table[i] = table[i] - table[pivot_row] * table[i, pivot_col]


