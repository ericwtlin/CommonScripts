import numpy as np

class StreamingRecorder():
    def __init__(self, names):
        """

        Args:
            names:  ['prediction', ... ]
        """
        self.__names = names
        self.__operators = dict()
        self.__recorder = dict()
        for name in names:
            self.__recorder[name] = []

    def record(self, name, values):
        self.__recorder[name].extend(values)

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
            return self.__recorder[name]
        elif operator == 'mean':
            return np.mean(self.__recorder[name])
        elif operator == 'sum':
            return np.sum(self.__recorder[name])


if __name__ == "__main__":
    streaming_recorder = StreamingRecorder(['prediction'])
    streaming_recorder.record('prediction', [1, 2, 3])
    streaming_recorder.record('prediction', [4, 5, 6])
    print(streaming_recorder.get('prediction', 'origin'))

