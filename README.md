# Commonsense Validation and Explanation (ComVE)

This is the official repo for SemEval 2020 Task 4: Commonsense Validation and Explanation.

This task is inspired and extension of the ACL 2019 paper: Does It Make Sense? And Why? A Pilot Study for Sense Making and Explanation. [link](https://arxiv.org/abs/1906.00363)

Welcome to pariticipate on our Codalab competition [here](https://competitions.codalab.org/competitions/21080)!

All participants are welcome to check and raise data errors at https://github.com/wangcunxiang/SemEval2020-Task4-Commonsense-Validation-and-Explanation/issues/9

## Introduction

The task is to directly test whether a system can differentiate natural language statements that make sense from those that do not make sense. We designed three subtasks. The first task is to choose from two natural language statements with similar wordings which one makes sense and which one does not make sense; The second task is to find the key reason from three options why a given statement does not make sense; The third task asks machine to generate the reasons and we use BLEU to evaluate them.

The detailed description of the task can be found in [Task Proposal](./TaskProposal.pdf).

### Example

#### Task A: Commonsense Validation

Which statement of the two is against common sense?

- Statement 1: He put a turkey into the fridge. *(correct)*
- Statement 2: He put an elephant into the fridge.

#### Task B: Commonsense Explanation (Multi-Choice)

Select the most corresponding reason why this statement is against common sense.

- Statement: He put an elephant into the fridge.

- Reasons:

  - **A**: An elephant is much bigger than a fridge. *(correct)*
  - **B**: Elephants are usually white while fridges are usually white.
  - **C**: An elephant cannot eat a fridge.

#### Task C: Commonsense Explanation (Generation)

Generate the reason why this statement is against common sense and we will use BELU to evaluate it.

- Statement: He put an elephant into the fridge.

- Referential Reasons:

  1. An elephant is much bigger than a fridge.
  2. A fridge is much smaller than an elephant.
  3. Most of the fridges aren’t large enough to contain an elephant.

## Evaluation

Subtask A and B will be evaluated using **accuracy**. Subtask C will be evaluated using BLEU score.

## Deadlines
 - 19 February 2020: Evaluation start*
 - 11 March 2020: Evaluation end*
 - 18 March 2020: Results posted
 - 15 May 2020 (UTC-12 23:59): System description paper submissions due
 - 22 May 2020(UTC-12 23:59): Task description paper submissions due
 - 24 Jun 2020(UTC-12 23:59): Author notifications
 - 8 Jul 2020(UTC-12 23:59): Camera ready submissions due
 - 12-13 December 2020:  SemEval 2020

## Citation
If you find this project helpful, you can cite
```bib
@inproceedings{wang-etal-2020-semeval,
    title = "{S}em{E}val-2020 Task 4: Commonsense Validation and Explanation",
    author = "Wang, Cunxiang  and
      Liang, Shuailong  and
      Jin, Yili  and
      Wang, Yilong  and
      Zhu, Xiaodan  and
      Zhang, Yue",
    booktitle = "Proceedings of The 14th International Workshop on Semantic Evaluation",
    year = "2020",
    publisher = "Association for Computational Linguistics",
}
```
as well as
```bib
 @inproceedings{wang-etal-2019-make,
    title = "Does it Make Sense? And Why? A Pilot Study for Sense Making and Explanation",
    author = "Wang, Cunxiang  and
      Liang, Shuailong  and
      Zhang, Yue  and
      Li, Xiaonan  and
      Gao, Tian",
    booktitle = "Proceedings of the 57th Annual Meeting of the Association for Computational Linguistics",
    month = jul,
    year = "2019",
    address = "Florence, Italy",
    publisher = "Association for Computational Linguistics",
    url = "https://www.aclweb.org/anthology/P19-1393",
    pages = "4020--4026",
    abstract = "Introducing common sense to natural language understanding systems has received increasing research attention. It remains a fundamental question on how to evaluate whether a system has the sense-making capability. Existing benchmarks measure common sense knowledge indirectly or without reasoning. In this paper, we release a benchmark to directly test whether a system can differentiate natural language statements that make sense from those that do not make sense. In addition, a system is asked to identify the most crucial reason why a statement does not make sense. We evaluate models trained over large-scale language modeling tasks as well as human performance, showing that there are different challenges for system sense-making.",
}
 ```


## License

The dataset is distributed under the [CC BY-SA 4.0](http://creativecommons.org/licenses/by-sa/4.0/legalcode) license.
