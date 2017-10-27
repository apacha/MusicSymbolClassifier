from sklearn import datasets
from sklearn.datasets import make_multilabel_classification
from sklearn.metrics.tests.test_classification import make_prediction
from sklearn.utils.testing import assert_warns_message, assert_equal

from reporting.sklearn_reporting import classification_report
import numpy as np


def test_classification_report_multiclass():
    # Test performance report
    iris = datasets.load_iris()
    y_true, y_pred, _ = make_prediction(dataset=iris, binary=False)

    # print classification report with class names
    expected_report = """\
              precision    recall  f1-score   support

      setosa       0.83      0.79      0.81        24
  versicolor       0.33      0.10      0.15        31
   virginica       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(
        y_true, y_pred, labels=np.arange(len(iris.target_names)),
        target_names=iris.target_names)
    assert_equal(report, expected_report)
    # print classification report with label detection
    expected_report = """\
              precision    recall  f1-score   support

           0       0.83      0.79      0.81        24
           1       0.33      0.10      0.15        31
           2       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_digits():
    # Test performance report with added digits in floating point values
    iris = datasets.load_iris()
    y_true, y_pred, _ = make_prediction(dataset=iris, binary=False)

    # print classification report with class names
    expected_report = """\
              precision    recall  f1-score   support

      setosa    0.82609   0.79167   0.80851        24
  versicolor    0.33333   0.09677   0.15000        31
   virginica    0.41860   0.90000   0.57143        20

weighted avg    0.51375   0.53333   0.47310        75
"""
    report = classification_report(
        y_true, y_pred, labels=np.arange(len(iris.target_names)),
        target_names=iris.target_names, digits=5)
    assert_equal(report, expected_report)
    # print classification report with label detection
    expected_report = """\
              precision    recall  f1-score   support

           0       0.83      0.79      0.81        24
           1       0.33      0.10      0.15        31
           2       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_string_label():
    y_true, y_pred, _ = make_prediction(binary=False)

    y_true = np.array(["blue", "green", "red"])[y_true]
    y_pred = np.array(["blue", "green", "red"])[y_pred]

    expected_report = """\
              precision    recall  f1-score   support

        blue       0.83      0.79      0.81        24
       green       0.33      0.10      0.15        31
         red       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)

    expected_report = """\
              precision    recall  f1-score   support

           a       0.83      0.79      0.81        24
           b       0.33      0.10      0.15        31
           c       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(y_true, y_pred,
                                   target_names=["a", "b", "c"])
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_unicode_label():
    y_true, y_pred, _ = make_prediction(binary=False)

    labels = np.array([u"blue\xa2", u"green\xa2", u"red\xa2"])
    y_true = labels[y_true]
    y_pred = labels[y_pred]

    expected_report = u"""\
              precision    recall  f1-score   support

       blue\xa2       0.83      0.79      0.81        24
      green\xa2       0.33      0.10      0.15        31
        red\xa2       0.42      0.90      0.57        20

weighted avg       0.51      0.53      0.47        75
"""
    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_long_string_label():
    y_true, y_pred, _ = make_prediction(binary=False)

    labels = np.array(["blue", "green" * 5, "red"])
    y_true = labels[y_true]
    y_pred = labels[y_pred]

    expected_report = """\
                           precision    recall  f1-score   support

                     blue       0.83      0.79      0.81        24
greengreengreengreengreen       0.33      0.10      0.15        31
                      red       0.42      0.90      0.57        20

             weighted avg       0.51      0.53      0.47        75
"""

    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)


def test_classification_report_labels_target_names_unequal_length():
    y_true = [0, 0, 2, 0, 0]
    y_pred = [0, 2, 2, 0, 0]
    target_names = ['class 0', 'class 1', 'class 2']

    assert_warns_message(UserWarning,
                         "labels size, 2, does not "
                         "match size of target_names, 3",
                         classification_report,
                         y_true, y_pred, target_names=target_names)


def test_multilabel_classification_report():
    n_classes = 4
    n_samples = 50

    _, y_true = make_multilabel_classification(n_features=1,
                                               n_samples=n_samples,
                                               n_classes=n_classes,
                                               random_state=0)

    _, y_pred = make_multilabel_classification(n_features=1,
                                               n_samples=n_samples,
                                               n_classes=n_classes,
                                               random_state=1)

    expected_report = """\
              precision    recall  f1-score   support

           0       0.50      0.67      0.57        24
           1       0.51      0.74      0.61        27
           2       0.29      0.08      0.12        26
           3       0.52      0.56      0.54        27

weighted avg       0.45      0.51      0.46       104
"""

    report = classification_report(y_true, y_pred)
    assert_equal(report, expected_report)


def test_multilabel_classification_report_with_samples_averaging():
    n_classes = 4
    n_samples = 50

    _, y_true = make_multilabel_classification(n_features=1,
                                               n_samples=n_samples,
                                               n_classes=n_classes,
                                               random_state=0)

    _, y_pred = make_multilabel_classification(n_features=1,
                                               n_samples=n_samples,
                                               n_classes=n_classes,
                                               random_state=1)

    expected_report = """\
             precision    recall  f1-score   support

          0       0.50      0.67      0.57        24
          1       0.51      0.74      0.61        27
          2       0.29      0.08      0.12        26
          3       0.52      0.56      0.54        27

samples avg       0.46      0.42      0.40       104
"""

    report = classification_report(y_true, y_pred, average='samples')
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_micro_averaging():
    # Test performance report
    iris = datasets.load_iris()
    y_true, y_pred, _ = make_prediction(dataset=iris, binary=False)

    # print classification report with class names
    expected_report = """\
            precision    recall  f1-score   support

    setosa       0.83      0.79      0.81        24
versicolor       0.33      0.10      0.15        31
 virginica       0.42      0.90      0.57        20

 micro avg       0.53      0.53      0.53        75
"""
    report = classification_report(
        y_true, y_pred, labels=np.arange(len(iris.target_names)),
        target_names=iris.target_names, average='micro')
    assert_equal(report, expected_report)


def test_classification_report_multiclass_with_macro_averaging():
    # Test performance report
    iris = datasets.load_iris()
    y_true, y_pred, _ = make_prediction(dataset=iris, binary=False)

    # print classification report with class names
    expected_report = """\
            precision    recall  f1-score   support

    setosa       0.83      0.79      0.81        24
versicolor       0.33      0.10      0.15        31
 virginica       0.42      0.90      0.57        20

 macro avg       0.53      0.60      0.51        75
"""
    report = classification_report(
        y_true, y_pred, labels=np.arange(len(iris.target_names)),
        target_names=iris.target_names, average='macro')
    assert_equal(report, expected_report)


def test_classification_report_binary_averaging():
    y_true = [0, 1, 1, 1, 0, 1, 1, 0]
    y_pred = [0, 0, 1, 1, 1, 0, 1, 0]

    # print classification report with class names
    expected_report = """\
            precision    recall  f1-score   support

         0       0.50      0.67      0.57         3
         1       0.75      0.60      0.67         5

binary avg       0.75      0.60      0.67         8
"""

    report = classification_report(y_true, y_pred, average='binary')
    assert_equal(report, expected_report)
