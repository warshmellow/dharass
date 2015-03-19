'''
Contains some processing code to data from scikit-learn matrices to
work with OpenPR-NBEM, Naive Bayes Expectation Maximization library
'''

import ipdb
import numpy as np
import itertools


def get_nonzero_indices_and_counts(X, shift=0):
    '''
    Takes sparse matrix and returns list, where each list is either
    empty or contains the pairs (index + shift, count)
    '''
    # Convert to CSR matrix format and Sort indices
    X = X.tocsr().sorted_indices()

    # Get nonzero entries
    nonzero_row_cols = zip(*X.nonzero())

    # Get long list of lists of (idx, count) for matrix
    result = []
    i = 0
    for k, items in itertools.groupby(nonzero_row_cols, lambda x: x[0]):
        while i < k:
            result.append([])
            i += 1

        nonzero_idx = np.array(sorted(map(lambda x: x[1], list(items))))
        nonzero_entries = np.array(X[k][X[k] != 0])[0]
        idx_count_lst = zip(nonzero_idx + shift, nonzero_entries)
        result.append(idx_count_lst)

        i += 1
    # Return list
    return result


def format_nonzero_row(nonzero_entries,
                       label=None,
                       label_shift=0,
                       default_missing_label=0):
    'Format output of get_nonzero_indices_and_counts to be printable row'
    lst_of_terms = []
    if label is None:
        lst_of_terms.append(str(default_missing_label))
    else:
        lst_of_terms.append(str(label + label_shift))
    lst_of_terms.append('\t')
    for idx, val in nonzero_entries:
        lst_of_terms.append(str(int(idx)) + ':' + str(int(val)))
        lst_of_terms.append(' ')
    return ''.join(lst_of_terms).rstrip()


def convert_vectorized_to_printable_rows(X, y=None):
    '''
    Takes vectorized (sparse) matrix and labels,
    and returns list of formatted strings of rows for NBEM.
    If missing labels, then label will be 0
    '''
    results = get_nonzero_indices_and_counts(X, shift=1)

    if y is None:
        rows = []
        for result in results:
            rows.append(format_nonzero_row(result))
    else:
        rows = []
        for row_num, result in enumerate(results):
            rows.append(format_nonzero_row(result, y[row_num], label_shift=1))
    return rows


def print_printable_rows_to_file(rows, filename, header=None):
    'Prints printable rows to file, prefacing with header'
    with open(filename, 'w') as f:
        if header:
            f.write(header + '\n')
        for row in rows:
            f.write(row + '\n')


def print_vectorized_to_file(filename, X, y=None, header=None):
    # Convert vectorized X to printable rows
    # Then print to file
    print_printable_rows_to_file(
        convert_vectorized_to_printable_rows(X, y), filename, header)
