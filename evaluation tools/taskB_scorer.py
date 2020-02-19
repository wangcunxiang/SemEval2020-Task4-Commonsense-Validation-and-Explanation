#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Shuailong
# @Email: liangshuailong@gmail.com
# @Date: 2019-08-14 15:26:12
# @Last Modified by: Shuailong
# @Last Modified time: 2019-08-14 15:51:40
# Modified from https://github.com/allenai/aristo-leaderboard/blob/master/openbookqa/evaluator/evaluator.py

import argparse
import csv
from typing import Dict, List
import logging
import sys
import json


EXIT_STATUS_ANSWERS_MALFORMED = 1
EXIT_STATUS_PREDICTIONS_MALFORMED = 2
EXIT_STATUS_PREDICTIONS_EXTRA = 3
EXIT_STATUS_PREDICTION_MISSING = 4


def calculate_accuracy(gold_labels: Dict[str, str], predictions: Dict[str, List[str]]) -> float:
    score = 0.0

    for instance_id, answer in gold_labels.items():
        try:
            predictions_for_current = predictions[instance_id]
        except KeyError:
            logging.error("Missing prediction for question '%s'.", instance_id)
            sys.exit(EXIT_STATUS_PREDICTION_MISSING)

        if answer == predictions_for_current:
            score += 1.0 / len(predictions_for_current)

        del predictions[instance_id]

    if len(predictions) > 0:
        logging.error("Found %d extra predictions, for example: %s", len(
            predictions), ", ".join(list(predictions.keys())[:3]))
        sys.exit(EXIT_STATUS_PREDICTIONS_EXTRA)

    return score / len(gold_labels)


def read_gold(filename: str) -> Dict[str, str]:
    answers = {}

    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    answer = row[1]
                except IndexError as e:
                    logging.error(
                        "Error reading value from CSV file %s on line %d: %s", filename, reader.line_num, e)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                if instance_id in answers:
                    logging.error("Key %s repeated in %s",
                                  instance_id, filename)
                    sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

                answers[instance_id] = answer

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    if len(answers) == 0:
        logging.error("No answers found in file %s", filename)
        sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    return answers


def read_predictions(filename: str) -> Dict[str, List[str]]:
    predictions = {}

    with open(filename, "rt", encoding="UTF-8", errors="replace") as f:
        reader = csv.reader(f)
        try:
            for row in reader:
                try:
                    instance_id = row[0]
                    prediction = row[1]
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

                # prediction labels cannot be empty strings
                if prediction == "":
                    logging.error("Key %s has empty labels for prediction in file %s on line %d",
                                  instance_id, filename, reader.line_num)
                    sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)
                predictions[instance_id] = prediction

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_PREDICTIONS_MALFORMED)

    return predictions


def main():
    gold_labels = read_gold(args.gold_labels)
    pred_labels = read_predictions(args.pred_labels)
    accuracy = calculate_accuracy(gold_labels, pred_labels)

    print(f'Accuracy: {accuracy*100:.4f}%')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='SemEval 2020 Task 4 subtask B official evaluation script')
    parser.add_argument('--gold-labels', '-g', help='gold label in csv format')
    parser.add_argument('--pred-labels', '-p',
                        help='prediction labels in csv format')
    args = parser.parse_args()
    main()
