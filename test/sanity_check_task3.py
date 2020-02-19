#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# @Author: Shuailong
# @Email: liangshuailong@gmail.com
# @Date: 2019-08-14 23:21:08
# @Last Modified by: Shuailong
# @Last Modified time: 2019-08-14 23:21:32

from typing import List
import argparse
import logging
import csv
import sys


EXIT_STATUS_ANSWERS_MALFORMED = 1
EXIT_STATUS_PREDICTIONS_MALFORMED = 2
EXIT_STATUS_PREDICTIONS_EXTRA = 3
EXIT_STATUS_PREDICTION_MISSING = 4


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
                elif len(tokens) == 1:
                    logging.warning(
                        "1 reference sentence in file %s on line %d", filename, reader.line_num)
                elif len(tokens) == 2:
                    logging.warning(
                        "2 reference sentences in file %s on line %d", filename, reader.line_num)

                references[instance_id] = tokens

        except csv.Error as e:
            logging.error('file %s, line %d: %s', filename, reader.line_num, e)
            sys.exit(EXIT_STATUS_ANSWERS_MALFORMED)

    return references


def main():
    read_references(args.references)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description='Sanity check for subtask C data')
    parser.add_argument('--references', '-r', help='dataset file')
    args = parser.parse_args()
    main()
