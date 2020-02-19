#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Shuailong
# @Email: liangshuailong@gmail.com
# @Date: 2019-08-14 15:26:18
# @Last Modified by: Shuailong
# @Last Modified time: 2019-08-14 15:54:54
# Modified from https://github.com/tensorflow/nmt/blob/master/nmt/scripts/bleu.py

from typing import List, Dict
import csv
import logging
import sys
import argparse
import collections
import math

EXIT_STATUS_ANSWERS_MALFORMED = 1
EXIT_STATUS_PREDICTIONS_MALFORMED = 2
EXIT_STATUS_PREDICTIONS_EXTRA = 3
EXIT_STATUS_PREDICTION_MISSING = 4


def _get_ngrams(segment, max_order):
    """Extracts all n-grams upto a given maximum order from an input segment.
    Args:
        segment: text segment from which n-grams will be extracted.
        max_order: maximum length in tokens of the n-grams returned by this
        methods.
    Returns:
        The Counter containing all n-grams upto max_order in segment
        with a count of how many times each n-gram occurred.
    """
    ngram_counts = collections.Counter()
    for order in range(1, max_order + 1):
        for i in range(0, len(segment) - order + 1):
            ngram = tuple(segment[i:i+order])
            ngram_counts[ngram] += 1
    return ngram_counts


def _compute_bleu(reference_corpus, translation_corpus, max_order=4, smooth=False):
    """Computes BLEU score of translated segments against one or more references.
    Args:
        reference_corpus: list of lists of references for each translation. Each
            reference should be tokenized into a list of tokens.
        translation_corpus: list of translations to score. Each translation
            should be tokenized into a list of tokens.
        max_order: Maximum n-gram order to use when computing BLEU score.
        smooth: Whether or not to apply Lin et al. 2004 smoothing.
    Returns:
        3-Tuple with the BLEU score, n-gram precisions, geometric mean of n-gram
            precisions and brevity penalty.
    """
    matches_by_order = [0] * max_order
    possible_matches_by_order = [0] * max_order
    reference_length = 0
    translation_length = 0
    for (references, translation) in zip(reference_corpus, translation_corpus):
        reference_length += min(len(r) for r in references)
        translation_length += len(translation)

        merged_ref_ngram_counts = collections.Counter()
        for reference in references:
            merged_ref_ngram_counts |= _get_ngrams(reference, max_order)
        translation_ngram_counts = _get_ngrams(translation, max_order)
        overlap = translation_ngram_counts & merged_ref_ngram_counts
        for ngram in overlap:
            matches_by_order[len(ngram)-1] += overlap[ngram]
        for order in range(1, max_order+1):
            possible_matches = len(translation) - order + 1
            if possible_matches > 0:
                possible_matches_by_order[order-1] += possible_matches

    precisions = [0] * max_order
    for i in range(0, max_order):
        if smooth:
            precisions[i] = ((matches_by_order[i] + 1.) /
                             (possible_matches_by_order[i] + 1.))
        else:
            if possible_matches_by_order[i] > 0:
                precisions[i] = (float(matches_by_order[i]) /
                                 possible_matches_by_order[i])
            else:
                precisions[i] = 0.0

    if min(precisions) > 0:
        p_log_sum = sum((1. / max_order) * math.log(p) for p in precisions)
        geo_mean = math.exp(p_log_sum)
    else:
        geo_mean = 0

    ratio = float(translation_length) / reference_length

    if ratio > 1.0:
        bp = 1.
    else:
        bp = math.exp(1 - 1. / ratio)

    bleu = geo_mean * bp

    return (bleu, precisions, bp, ratio, translation_length, reference_length)


def calculate_bleu(references: Dict[str, List[List[str]]],
                   predictions: Dict[str, List[str]],
                   max_order=4,
                   smooth=False) -> float:

    reference_corpus = []
    prediction_corpus = []

    for instance_id, reference_sents in references.items():
        try:
            prediction_sent = predictions[instance_id]
        except KeyError:
            logging.error("Missing prediction for instance '%s'.", instance_id)
            sys.exit(EXIT_STATUS_PREDICTION_MISSING)

        del predictions[instance_id]

        prediction_corpus.append(prediction_sent)
        reference_corpus.append(reference_sents)

    if len(predictions) > 0:
        logging.error("Found %d extra predictions, for example: %s", len(predictions),
                      ", ".join(list(predictions.keys())[:3]))
        sys.exit(EXIT_STATUS_PREDICTIONS_EXTRA)

    score = _compute_bleu(reference_corpus, prediction_corpus,
                          max_order=max_order, smooth=smooth)[0]

    return score


def read_references(filename: str) -> List[List[List[str]]]:
    references = {}
    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    references_raw1 = row[1]
                    references_raw2 = row[2]
                    references_raw3 = row[3]
                except IndexError as e:
                    logging.error(
                        "Error reading value from CSV file %s on line %d: %s", filename, reader.line_num, e)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                if instance_id in references:
                    logging.error("Key %s repeated in file %s on line %d",
                                  instance_id, filename, reader.line_num)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                if instance_id == "":
                    logging.error(
                        "Key is empty in file %s on line %d", filename, reader.line_num)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                tokens = []
                for ref in [references_raw1, references_raw2, references_raw3]:
                    if ref:
                        tokens.append(ref.split())

                if len(tokens) == 0:
                    logging.error(
                        "No reference sentence in file %s on line %d", filename, reader.line_num)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                references[instance_id] = tokens

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    return references


def read_predictions(filename: str) -> List[List[str]]:
    predictions = {}
    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    prediction_raw = row[1]
                except IndexError as e:
                    logging.error(
                        "Error reading value from CSV file %s on line %d: %s", filename, reader.line_num, e)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                if instance_id in predictions:
                    logging.error("Key %s repeated in file %s on line %d",
                                  instance_id, filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                if instance_id == "":
                    logging.error(
                        "Key is empty in file %s on line %d", filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

                if prediction_raw == "":
                    logging.warning("Key % s has empty prediction in file % s on line % d",
                                    instance_id, filename, reader.line_num)

                tokens = prediction_raw.split()
                predictions[instance_id] = tokens

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

    return predictions


def main():
    references = read_references(args.references)
    predictions = read_predictions(args.predictions)

    bleu = calculate_bleu(references, predictions,
                          max_order=args.max_order, smooth=args.smooth)

    print(f'BLEU score: {bleu*100:.4f}.')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SemEval 2020 Task 4 subtask C official evaluation script')
    parser.add_argument('--references', '-r',
                        help='reference file in csv format')
    parser.add_argument('--predictions', '-p',
                        help='prediction file in csv format')
    parser.add_argument(
        '--max_order', default=4, type=int, help='Maximum n-gram order to use when computing BLEU score')
    parser.add_argument('--smooth', action='store_true',
                        help='Whether or not to apply Lin et al. 2004 smoothing')
    args = parser.parse_args()
    main()
