# Dynamic Branch Prediction

This repository contains simulations for various dynamic branch predictors commonly used in computer architecture. The branch predictors included are Smith n-bit, Bimodal, GShare, and Hybrid branch predictors.


## Smith n-bit Predictor

### Description
The Smith n-bit predictor is a type of saturating counter predictor. It uses a counter of n bits to keep track of the history of a branch. The counter is incremented or decremented based on the branch outcome.

### Usage
To simulate the Smith n-bit predictor, run the following command in the terminal:

```
python3 sim.py smith <B> <trace file>
```
where B is the number of counter bits used for prediction and trace file is name of benchmark file (e.g., gcc_trace.txt)

## Bimodal Predictor

### Description
The Bimodal predictor is a simple branch predictor that uses a table of saturating counters. Each entry in the table corresponds to a particular branch instruction. The predictor predicts the outcome based on the value stored in the corresponding table entry.

### Usage
To simulate the Bimodal branch predictor, run the following command in the terminal:

```
python3 sim.py bimodal <M> <trace file>
```

where M is the number of PC bits used to index the bimodal table

## GShare Predictor

### Description
The GShare predictor is a global history predictor that combines the global history with the branch instruction address. It uses a table of saturating counters to predict the branch outcomes.

### Usage
To simulate the GShare branch predictor, run the following command in the terminal:

```
python3 sim.py gshare <M> <N> <trace file>
```

where M and N are the number of PC bits and global branch history register bits used to index the gshare table, respectively

## Hybrid Predictor

### Description
The Hybrid predictor combines the predictions of multiple predictors, such as the Bimodal and GShare predictors, to improve overall accuracy. It uses a selector to determine which predictor's output to use for a given branch instruction.

### Usage
To simulate the Hybrid branch predictor, run the following command in the terminal:

```
python3 sim.py hybrid <K> <M1> <N> <M2> <trace file>
```
where K is the number of PC bits used to index the chooser table, M1 and N are the number of PC bits and global branch history register bits used to index the gshare table (respectively), and M2 is the number of PC bits used to index the bimodal table. 

