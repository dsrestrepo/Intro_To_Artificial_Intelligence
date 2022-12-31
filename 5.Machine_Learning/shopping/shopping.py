import csv
import sys
import numpy as np
import pandas as pd
import warnings

warnings.filterwarnings('ignore')

from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn import metrics

TEST_SIZE = 0.4


def main():

    # Check command-line arguments
    if len(sys.argv) != 2:
        sys.exit("Usage: python shopping.py data")

    # Load data from spreadsheet and split into train and test sets
    evidence, labels = load_data(sys.argv[1])
    X_train, X_test, y_train, y_test = train_test_split(
        evidence, labels, test_size=TEST_SIZE
    )

    # Train model and make predictions
    model = train_model(X_train, y_train)
    predictions = model.predict(X_test)
    sensitivity, specificity = evaluate(y_test, predictions)

    # Print results
    print(f"Correct: {(y_test == predictions).sum()}")
    print(f"Incorrect: {(y_test != predictions).sum()}")
    print(f"True Positive Rate: {100 * sensitivity:.2f}%")
    print(f"True Negative Rate: {100 * specificity:.2f}%")

# Function to convert visitor into int
def visitor_to_int(visitor):
    # if retunrning visitor returns 1
    if visitor == 'Returning_Visitor':
        return 1
    # otherwise returns 0
    else:
        return 0

def load_data(filename):
    """
    Load shopping data from a CSV file `filename` and convert into a list of
    evidence lists and a list of labels. Return a tuple (evidence, labels).

    evidence should be a list of lists, where each list contains the
    following values, in order:
        - Administrative, an integer
        - Administrative_Duration, a floating point number
        - Informational, an integer
        - Informational_Duration, a floating point number
        - ProductRelated, an integer
        - ProductRelated_Duration, a floating point number
        - BounceRates, a floating point number
        - ExitRates, a floating point number
        - PageValues, a floating point number
        - SpecialDay, a floating point number
        - Month, an index from 0 (January) to 11 (December)
        - OperatingSystems, an integer
        - Browser, an integer
        - Region, an integer
        - TrafficType, an integer
        - VisitorType, an integer 0 (not returning) or 1 (returning)
        - Weekend, an integer 0 (if false) or 1 (if true)

    labels should be the corresponding list of labels, where each label
    is 1 if Revenue is true, and 0 otherwise.
    """
    # read csv file
    dataset = pd.read_csv(filename)

    # Labels:
    # Take the column Revenue (to predict)
    labels = dataset.loc[:,'Revenue']
    # Replace values False for 0, and True for 1
    labels.replace({False: 0, True: 1}, inplace=True)
    # Convert to list
    labels = labels.tolist()

    # Evidence (Features):
    # Take all columns except Revenue
    evidence = dataset.loc[:,dataset.columns != 'Revenue']
    # Month to int
    evidence['Month'].replace({'Jan': 0, 'Feb': 1, 'Mar': 2, 'Apr': 3, 'May': 4, 'June': 5, 'Jul': 6, 'Aug': 7, 'Sep': 8, 'Oct': 9, 'Nov': 10, 'Dec': 11}, inplace=True)
    # VisitorType
    # Apply to the pandas series (column)
    evidence['VisitorType'] = evidence['VisitorType'].apply(lambda visitor: visitor_to_int(visitor))
    # Weekend
    evidence['Weekend'].replace({False: 0, True: 1}, inplace=True)
    #print(evidence.dtypes)
    # Convert the dataframe into a list
    evidence = evidence.values.tolist()

    return evidence, labels


def train_model(evidence, labels):
    """
    Given a list of evidence lists and a list of labels, return a
    fitted k-nearest neighbor model (k=1) trained on the data.
    """
    # Crete model with 1 neighbor
    K = 1
    model = KNeighborsClassifier(n_neighbors=K)
    model.fit(evidence, labels)
    return model

def evaluate(labels, predictions):
    """
    Given a list of actual labels and a list of predicted labels,
    return a tuple (sensitivity, specificty).

    Assume each label is either a 1 (positive) or 0 (negative).

    `sensitivity` should be a floating-point value from 0 to 1
    representing the "true positive rate": the proportion of
    actual positive labels that were accurately identified.

    `specificity` should be a floating-point value from 0 to 1
    representing the "true negative rate": the proportion of
    actual negative labels that were accurately identified.
    """
    # Convert to operate
    labels = np.array(labels)
    predictions = np.array(predictions)
    
    # https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
    # Get True negatives, false positives, false negatives and true positives 
    tn, fp, fn, tp = metrics.confusion_matrix(labels, predictions).ravel()

    # Sensitivity
    sensitivity = tp / (tp + fn)
    # Specificity
    specificity = tn / (tn + fp)

    return sensitivity, specificity


if __name__ == "__main__":
    main()
