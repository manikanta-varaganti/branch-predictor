"""
Module: bimodal.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module contains the simulator logic for bimodal branch predictor.
"""
import sys
from utils import *


class BimodalPredictor:
    def __init__(self, PC_bits, trace_file) -> None:
        self.predictions = 0
        self.mispredictions = 0
        self.PC_bits = int(PC_bits)
        self.bimodal_prediction_table_size = 2**self.PC_bits
        self.trace_file = trace_file
        self.bimodal_prediction_table = [
            4
        ] * self.bimodal_prediction_table_size  # initialize the prediction table

    # returns the index value for prediction table
    def get_index(self, address):
        return (int(address, 16) >> 2) & (
            (1 << self.PC_bits) - 1
        )  # obtain the last m bit address by discarding the lowest 2 bits

    # bimodal branch predictor logic
    def predict(self):
        with open("traces/" + self.trace_file, "r") as file:
            traces = file.readlines()
            for instruction in traces[:]:
                self.predictions += 1
                address, outcome = instruction.split(" ")
                actual_outcome = outcome.strip()

                index = self.get_index(address)
                pred_counter = self.bimodal_prediction_table[index]
                pred_outcome = self.predict_outcome(pred_counter)

                if actual_outcome != pred_outcome:
                    self.mispredictions += 1

                self.update_counter(actual_outcome, index)

    # predicts the outcome based on prediction counter
    def predict_outcome(self, counter):
        if counter >= 4:
            return "t"
        else:
            return "n"

    # updates the prediction counter at the index
    def update_counter(self, outcome, index):
        if outcome == "t":
            counter = self.bimodal_prediction_table[index] + 1
            self.bimodal_prediction_table[index] = min(7, counter)
        else:
            counter = self.bimodal_prediction_table[index] - 1
            self.bimodal_prediction_table[index] = max(0, counter)

    # write results to text file under output folder
    def write_results(self):
        file_op = open("output/bimodal_output.txt", "w")
        file_op.write("COMMAND\n")
        file_op.write(f"./sim bimodal {self.PC_bits} {self.trace_file}\n")
        file_op.write("OUTPUT\n")
        file_op.write(f"number of predictions:		{self.predictions}\n")
        file_op.write(f"number of mispredictions:	{self.mispredictions}\n")
        file_op.write(
            f"misprediction rate:		{ self.mispredictions / self.predictions * 100:.2f}%\n"
        )
        file_op.write(f"FINAL BIMODAL CONTENTS\n")
        for i in range(2**self.PC_bits):
            file_op.write(f"{i}\t{self.bimodal_prediction_table[i]}\n")
