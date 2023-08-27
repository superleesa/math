__author__ = "Satoshi Kashima"
__studentid__ = "32678940"


from linear_optimization import initialize_array, tabular_simplex
import sys
import numpy as np

def process_input(file_content: list[str]) -> tuple[int, int, list, list[list[int]], list[int]]:
    """
    Process the text content to retrieve data needed for tabular simplex.
    :param file_content: the content of the file. should be strings in a list
    :return: num_decision_variables, num_constraints, objectives, lhs_coefs, rhs_coefs
    """
    num_decision_variables = int(file_content[1])
    num_constraints = int(file_content[3])
    objectives = list(map(int, file_content[5].split(", ")))

    assert len(objectives) == num_decision_variables, "number of decision variables specified and actual number different"

    # construct LHS
    lhs_coefs = []
    for i in range(7, 7+num_constraints):
        lhs_coefs.append(list(map(int, file_content[i].split(", "))))

    # construct RHS
    rhs_coefs = []
    for i in range(7+num_constraints+1, len(file_content)):
        rhs_coefs.append(int(file_content[i]))

    return num_decision_variables, num_constraints, objectives, lhs_coefs, rhs_coefs


def process_result(optimal_decisions: np.ndarray, optimal_objective: int) -> str:
    res = "# optimalDecisions\n" + ", ".join(list(map(str, optimal_decisions))) + "\n" \
        + "# optimalObjective\n" + str(optimal_objective)

    return res

if __name__ == "__main__":
    _, filename = sys.argv
    with open(filename) as file:
        inp = process_input(file.readlines())
        optimal_decisions, optimal_objective = tabular_simplex(*initialize_array(*inp))

    oup_filename = "lpsolution.txt"
    with open(oup_filename, "w") as file:
        file.write(process_result(optimal_decisions, optimal_objective))
