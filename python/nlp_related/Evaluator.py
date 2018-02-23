from sklearn import metrics


class Evaluator(object):
    def __init__(self, metrics, pos_label=1):
        self.__metrics = metrics
        self.__pos_label = pos_label

        supported_metrics = self.get_supported_metrics()
        for metric in metrics:
            if not metric in supported_metrics:
                raise Exception("The metric %s is not supported. Supported metrics are: %s" % (metric, supported_metrics))

    def evaluate(self, y_true, y_pred, y_pred_score, formatting=False):
        """

        Args:
            y_true:
            y_pred:
            y_pred_score:
            formatting:  if True: return string like "accuracy: 0.xxx; auc: 0.xxx"
                         if False: return dict describes each metric

        Returns:

        """
        result = dict()

        for metric in self.__metrics:
            result[metric] = getattr(self, metric)(y_true, y_pred, y_pred_score)

        if formatting is True:
            ret = self.format_result(result)
        else:
            ret = result
        return ret

    def get_supported_metrics(self):
        except_methods = ["evaluate", "format_result", "get_supported_metrics"]
        supported_metrics = []
        for name in dir(self):
            if name.startswith("_") is False and not name in except_methods:
                supported_metrics.append(name)
        return supported_metrics

    def format_result(self, result):
        return "; ".join(["%s: %.6f" % (metric, result[metric]) for metric in self.__metrics])

    def auc(self, y_true, y_pred, y_pred_score):
        fpr, tpr, thresholds = metrics.roc_curve(y_true, y_pred_score, pos_label=self.__pos_label)
        return metrics.auc(fpr, tpr)

    def accuracy(self, y_true, y_pred, y_pred_score):
        return metrics.accuracy_score(y_true, y_pred)

