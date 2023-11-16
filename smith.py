"""
Module: smith.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module contains the simulator logic for smith n-bit branch predictor.
"""
import sys


class SmithPredictor:
    def __init__(self, no_of_bits, trace_file) -> None:
        self.predictions = 0
        self.mispredictions = 0
        self.trace_file = trace_file
        self.num_bits = int(no_of_bits)
        self.prediction_counter = 2 ** (self.num_bits - 1)  # intialize the counter

    # smith n-bit predictor logic
    def predict(self):
        with open("traces/" + self.trace_file, "r") as file:
            traces = file.readlines()
            for instruction in traces[:]:
                self.predictions += 1
                address, outcome = instruction.split(" ")
                actual_outcome = outcome.strip()
                pred = self.predict_outcome(counter=self.prediction_counter)

                if pred != actual_outcome:
                    self.mispredictions += 1
                self.update_counter(actual_outcome)

    # updates the prediction smith n-bit counter
    def update_counter(self, outcome):
        if outcome == "t":
            self.prediction_counter += 1
            self.prediction_counter = min(
                ((2**self.num_bits) - 1), self.prediction_counter
            )
        else:
            self.prediction_counter -= 1
            self.prediction_counter = max(0, self.prediction_counter)

    # predict the outcome based on prediction counter
    def predict_outcome(self, counter):
        if counter >= 2 ** (self.num_bits - 1):
            return "t"
        else:
            return "n"

    # write results to text file under output folder
    def write_results(self):
        file_op = open("output/smith_output.txt", "w")
        file_op.write("COMMAND\n")
        file_op.write(f"./sim smith {self.num_bits} {self.trace_file}\n")
        file_op.write("OUTPUT\n")
        file_op.write(f"number of predictions:		{self.predictions}\n")
        file_op.write(f"number of mispredictions:	{self.mispredictions}\n")
        file_op.write(
            f"misprediction rate:		{ self.mispredictions / self.predictions * 100:.2f}%\n"
        )
        file_op.write(f"FINAL COUNTER CONTENT:		{self.prediction_counter}\n")
