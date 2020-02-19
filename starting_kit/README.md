# Starting Kit

Welcome to use the starting kit for Commonsense Validation and Explanation!

## Data format

The file format for all three subtasks are csv.

For subtask A, each row of the csv file contains 3 fields: `id`, `sent0`, `sent1`, which are the ID of the instance, and two input sentences. The output file contains no header, and each row contains the id and the index of the sentence which makes sense.

For subtask B, each row of the csv file contains 5 fields: `id`, `FalseSent`, `OptionA`, `OptionB` , `OptionC`, which are the ID of the instance, the nonsensical sentence, and three reasons why the sentence does not make sense. The output contains no header, and each row contains the id and label of the correct reason.

For subtask C, each row of the csv file contains 2 fields: `id`, `FalseSent`, which are the ID of the instance, and the nonsensical sentence. The output file has no header, and each output file contains ID and the generated reason.

Please check the `sample_data` folder for the sample input data format, and `sample_submission_subtaskA`, `sample_submission_subtaskB` and `sample_submission_subtaskC` for the submission file format.

Note that the evaluation program accepts result for only 1 subtask, and exact the same file name as the sample should be used when submitting your own results. The evaluation program will choose different evaluation metrics and referenece data according to the file name.

A very common error is to include an extra subdirectory in your submission. Consider using the commands below to avoid that:

```bash
cd sample_submission_subtaskA
zip ../submission.zip *
cd ..
```

If you need any help, feel free to post at https://groups.google.com/d/forum/semeval-2020-task-4-all.  
