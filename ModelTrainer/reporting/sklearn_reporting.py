import warnings
import numpy as np
import sklearn
from sklearn.metrics import precision_recall_fscore_support
from sklearn.utils.multiclass import unique_labels


def classification_report(y_true, y_pred, labels=None, target_names=None,
                          sample_weight=None, average=None, digits=2):
    """Build a text report showing the main classification metrics

    Read more in the :ref:`User Guide <classification_report>`.

    Parameters
    ----------
    y_true : 1d array-like, or label indicator array / sparse matrix
        Ground truth (correct) target values.

    y_pred : 1d array-like, or label indicator array / sparse matrix
        Estimated targets as returned by a classifier.

    labels : array, shape = [n_labels]
        Optional list of label indices to include in the report.

    target_names : list of strings
        Optional display names matching the labels (same order).

    sample_weight : array-like of shape = [n_samples], optional
        Sample weights.

    average : string, [None (default), 'binary', 'micro', 'macro', 'samples', \
                       'weighted']
        If ``None``, the scores for each class are returned. Otherwise, this
        determines the type of averaging performed on the data:

        ``'binary'``:
            Only report results for the class specified by ``pos_label``.
            This is applicable only if targets (``y_{true,pred}``) are binary.
        ``'micro'``:
            Calculate metrics globally by counting the total true positives,
            false negatives and false positives.
        ``'macro'``:
            Calculate metrics for each label, and find their unweighted
            mean.  This does not take label imbalance into account.
        ``'weighted'``:
            Calculate metrics for each label, and find their average, weighted
            by support (the number of true instances for each label). This
            alters 'macro' to account for label imbalance; it can result in an
            F-score that is not between precision and recall.
        ``'samples'``:
            Calculate metrics for each instance, and find their average (only
            meaningful for multilabel classification where this differs from
            :func:`accuracy_score`).


    digits : int
        Number of digits for formatting output floating point values

    Returns
    -------
    report : string
        Text summary of the precision, recall, F1 score for each class.

        Note that in binary classification, recall of the positive class
        is also known as "sensitivity"; recall of the negative class is
        "specificity".

    Examples
    --------
    >>> from sklearn.metrics import classification_report
    >>> y_true = [0, 1, 2, 2, 2]
    >>> y_pred = [0, 0, 2, 2, 1]
    >>> target_names = ['class 0', 'class 1', 'class 2']
    >>> print(classification_report(y_true, y_pred, target_names=target_names))
                 precision    recall  f1-score   support
    <BLANKLINE>
        class 0       0.50      1.00      0.67         1
        class 1       0.00      0.00      0.00         1
        class 2       1.00      0.67      0.80         3
    <BLANKLINE>
    avg / total       0.70      0.60      0.61         5
    <BLANKLINE>

    """

    if labels is None:
        labels = unique_labels(y_true, y_pred)
    else:
        labels = np.asarray(labels)

    if target_names is not None and len(labels) != len(target_names):
        warnings.warn(
            "labels size, {0}, does not match size of target_names, {1}"
                .format(len(labels), len(target_names))
        )

    if average is None:
        last_line_heading = 'avg / total'
    else:
        last_line_heading = average + ' avg'

    if target_names is None:
        target_names = [u'%s' % l for l in labels]
    name_width = max(len(cn) for cn in target_names)
    width = max(name_width, len(last_line_heading), digits)

    headers = ["precision", "recall", "f1-score", "support"]
    head_fmt = u'{:>{width}s} ' + u' {:>9}' * len(headers)
    report = head_fmt.format(u'', *headers, width=width)
    report += u'\n\n'

    p, r, f1, s = precision_recall_fscore_support(y_true, y_pred,
                                                  labels=labels,
                                                  average=None,
                                                  sample_weight=sample_weight)

    row_fmt = u'{:>{width}s} ' + u' {:>9.{digits}f}' * 3 + u' {:>9}\n'
    rows = zip(target_names, p, r, f1, s)
    for row in rows:
        report += row_fmt.format(*row, width=width, digits=digits)

    report += u'\n'

    if average is None:
        p, r, f1 = np.average(p, weights=s), np.average(r, weights=s), np.average(f1, weights=s),
    else:
        p, r, f1, unused_s = precision_recall_fscore_support(y_true, y_pred,
                                                      labels=labels,
                                                      average=average,
                                                      sample_weight=sample_weight)

    report += row_fmt.format(last_line_heading,
                             p,
                             r,
                             f1,
                             np.sum(s),
                             width=width, digits=digits)

    return report


if __name__ == '__main__':
    y_true = [0, 1, 2, 2, 2]
    y_pred = [0, 0, 2, 2, 1]
    target_names = ['class 0', 'class 1', 'class 2']
    print(classification_report(y_true, y_pred, target_names=target_names))
    print(classification_report(y_true, y_pred, target_names=target_names, average='micro'))
    print(classification_report(y_true, y_pred, target_names=target_names, average='macro'))
    print(classification_report(y_true, y_pred, target_names=target_names, average='weighted'))
