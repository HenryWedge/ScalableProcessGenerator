from typing import List

from provider.transition.duration.duration_provider import DurationProvider, StaticDurationProvider
from utils.utils_types import BgColors, print_color


class TransitionMatrixBuilder:
    """
    A class for building transition matrices for Markov chains.
    """

    def __init__(self):
        """
        Initialize an empty transition matrix builder.
        """
        self.states = []
        self.transition_matrix = {}
        self.duration_matrix = {}

    def add_state(self, state: str, duration: DurationProvider = None, p: float = 0.0):
        """
         Add a new state to the transition matrix builder.

         :Args:
             state (str): The name of the new state.
             p (float): The probability of transitioning to itself.

         :returns:
             self
         """
        if state not in self.states:
            self.states.append(state)
            self.transition_matrix[state] = {}
            self.duration_matrix[state] = {}

            # probability to stay in the state is 0 and there is no time t = 0
            if p == 0.0 and duration is None:
                duration = StaticDurationProvider(0.0)
            # probability to stay in the state is not 0 and no t is give -> t is set to 1
            elif p != 0.0 and duration is None:
                duration = StaticDurationProvider(1.0)

            self.to(state, p=p, duration=duration)
        return self


    def add_transition(self, state, next_state, probability, time):
        if state in self.states and next_state in self.states:
            self.transition_matrix[state][next_state] = probability
            self.duration_matrix[state][next_state] = time

    def to(self, next_state: str, duration: DurationProvider, p: float):
        """
        Add a transition from the current state to the next state with a given probability.

        Args:
            next_state (str): The name of the next state.
            p (float): The probability of transitioning to the next state.
            t float | tuple[float, float]: the duration of the transition

        :returns:
            self
        """
        current_state = self.states[-1]
        self.transition_matrix[current_state][next_state] = p
        self.duration_matrix[current_state][next_state] = duration
        return self

    def to_matrix(self, from_list: dict, init_value) -> List[List]:
        """
        Convert the transition matrix to a 2D list of floats.

        :returns:
            List[List[float]]: The transition matrix as a 2D list of floats.
        """
        n: int = len(self.states)
        matrix: List[List] = [[init_value for _ in range(n)] for _ in range(n)]
        for i, state in enumerate(self.states):
            for j, next_state in enumerate(self.states):
                matrix[i][j] = from_list[state].get(next_state, init_value)
        return matrix

    def to_duration_matrix(self) -> List[List[DurationProvider]]:
        return self.to_matrix(self.duration_matrix, init_value=StaticDurationProvider(0))

    def to_transition_matrix(self) -> List[List[float]]:
        return self.to_matrix(self.transition_matrix, init_value=0.0)

    def print_transition_matrix(self):
        """
        Print the transition matrix in a human-readable format.
        """
        matrix = self.to_transition_matrix()
        n = len(self.states)
        # find the max length of state names
        max_state_len = len(max(self.states, key=len))
        print(" " * (max_state_len + 1), *self.states)
        for i, state in enumerate(self.states):
            # padding spaces to align the columns
            if round(sum(matrix[i])) == 1.0:
                print(f"{state:<{max_state_len}}  ", end="")
                for j in range(n):
                    print(f"{float(matrix[i][j]):<{max_state_len}} ", end="")
            else:
                print_color(f"{state:<{max_state_len}}  ", color=BgColors.FAIL, end="")
                for j in range(n):
                    print_color(f"{matrix[i][j]:<{max_state_len}} ", color=BgColors.FAIL, end="")
            print()

    def print_duration_matrix(self):
        """
        Print the transition matrix in a human-readable format.
        """
        matrix = self.to_duration_matrix()
        n = len(self.states)
        # find the max length of state names
        max_state_len = len(max(self.states, key=len))
        print(" " * (max_state_len + 1), *self.states)
        for i, state in enumerate(self.states):
            # padding spaces to align the columns
            print(f"{state:<{max_state_len}}  ", end="")
            for j in range(n):
                print(f"{str(round((matrix[i][j]).get_duration(), 2)):<{max_state_len}} ", end="")
            print()

    def print_transition_matrix_latex(self, selected_states: List[str] = None):
        """
        Print the transition matrix in LaTeX code format and copy to clipboard for selected states only.

        """

        if selected_states is None:
            selected_states = self.states

        matrix = self.to_transition_matrix()
        n = len(selected_states)

        latex_code = "\\begin{tabular}{||c " + " ".join(["c"] * n) + "||}\n"
        latex_code += "\\hline\n"
        latex_code += " & " + " & ".join(selected_states) + "\\\\\n"
        latex_code += "\\hline\n"
        for i, state in enumerate(selected_states):
            latex_code += state + " & " + " & ".join([f"{matrix[self.states.index(state)][self.states.index(j)]:.2f}" for j in selected_states]) + "\\\\\n"
            latex_code += "\\hline\n"
        latex_code += "\\end{tabular}"
        latex_code = latex_code.replace("_", " ")
        print(latex_code)
    def get_states(self):
        return self.states


