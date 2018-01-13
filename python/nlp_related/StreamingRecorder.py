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
        """ insert a col of multiple values

        Args:
            name:
            values:

        Returns:

        """
        if isinstance(values, list):
            self.__recorder[name].extend(values)
        else:
            self.__recorder[name].append(values)

    def record_one_row(self, values):
        """ insert a whole row

        Args:
            values: [col1, col2, col3, ...], each element can be either a list or a single number

        Returns:

        """
        assert len(self.__names) == len(values)
        for name, value in zip(self.__names, values):
            self.record(name, value)

    def get(self, name, operator=None):
        """

        Args:
            name:
            operator: has the same shape with names, supported operations:
                    None or 'origin': return the original values
                    'mean': return mean of the values
                    'sum': return sum of the values
                    'min': return min of the values
                    'max': return max of the values

        Returns:

        """

        if operator is None or operator == 'origin':
            return self.__recorder[name]
        elif operator == 'mean':
            return np.mean(self.__recorder[name])
        elif operator == 'sum':
            return np.sum(self.__recorder[name])
        elif operator == 'min':
            return np.min(self.__recorder[name])
        elif operator == 'max':
            return np.max(self.__recorder[name])


if __name__ == "__main__":
    streaming_recorder = StreamingRecorder(['prediction'])
    streaming_recorder.record('prediction', [1, 2, 3])
    streaming_recorder.record('prediction', [4, 5, 6])
    print(streaming_recorder.get('prediction', 'origin'))

