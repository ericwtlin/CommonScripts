import numpy as np

class StreamingRecorder():
    def __init__(self, names):
        """

        Args:
            names:  ['prediction', ... ]
        """
        self.names = names
        self.operators = dict()
        self.recorder = dict()
        for name in names:
            self.recorder[name] = []

    def record(self, name, values):
        self.recorder[name].extend(values)

    def get(self, name, operator=None):
        """

        Args:
            name:
            operator: has the same shape with names, supported operations:
                    None or 'origin': return the original values
                    'mean': return mean of the values
                    'sum': return sum of the values

        Returns:

        """

        if operator is None or operator == 'origin':
            return self.recorder[name]
        elif operator == 'mean':
            return np.mean(self.recorder[name])
        elif operator == 'sum':
            return np.sum(self.recorder[name])


