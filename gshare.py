"""
Module: gshare.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module contains the simulator logic for GShare branch predictor.
"""
import sys
from utils import *


class GSharePredictor:
    def __init__(self, PC_bits, bhr_bits, trace_file) -> None:
        self.predictions = 0
        self.mispredictions = 0
        self.PC_bits = int(PC_bits)
        self.bhr_bits = int(bhr_bits)
        self.trace_file = trace_file
        self.branch_history_register = "0" * self.bhr_bits
        self.gshare_prediction_table_size = 2**self.PC_bits
        self.gshare_prediction_table = [
            4
        ] * self.gshare_prediction_table_size  # initialize the gshare prediction table

    # performs xor operation on  bhr register and lowermost n pc bits
    def xor_operation(self, str1, str2):
        s1 = int(str1, 2)
        s2 = int(str2, 2)
        xor = s1 ^ s2
        return bin(xor)[2:].zfill(max(len(str1), len(str2)))

    # get the index value for prediction table
    def get_index(self, address):
        # get the first m bits by discarding last 2 bits in 32 bit binary address
        pc_address = hex_to_bin(address)[-2 - self.PC_bits : -2]
        # get the last n bits in binary address
        lowermost_pc_n_bits = pc_address[-self.bhr_bits :]
        # perform xor operation on bhr register and lowermost n pc bits
        xor_bits = self.xor_operation(lowermost_pc_n_bits, self.branch_history_register)
        # get the remaining m-n bits
        remaining_bits = pc_address[: self.PC_bits - self.bhr_bits]
        # concatenate the remaining m-n bits with xor bits to get m-bit index address
        index_bits = remaining_bits + xor_bits
        # return index value
        return int(index_bits, 2) % self.gshare_prediction_table_size

    # GShare branch predictor logic
    def predict(self):
        with open("traces/" + self.trace_file, "r") as file:
            traces = file.readlines()
            for instruction in traces[:]:
                self.predictions += 1
                address, outcome = instruction.split(" ")
                actual_outcome = outcome.strip()

                index = self.get_index(address)
                pred_counter = self.gshare_prediction_table[index]
                pred_outcome = self.predict_outcome(pred_counter)
                if actual_outcome != pred_outcome:
                    self.mispredictions += 1
                self.update_counter(actual_outcome, index)
                if actual_outcome == "t":
                    self.update_bhr("1")
                else:
                    self.update_bhr("0")

    # updates the prediction counter at the index
    def update_counter(self, outcome, index):
        if outcome == "t":
            counter = self.gshare_prediction_table[index] + 1
            self.gshare_prediction_table[index] = min(7, counter)
        else:
            counter = self.gshare_prediction_table[index] - 1
            self.gshare_prediction_table[index] = max(0, counter)

    # updates the branch history register by right shifting 1 bit and add outcome in MSB
    def update_bhr(self, outcome):
        bhr = self.branch_history_register[:-1]
        updated_bhr = outcome + bhr
        self.branch_history_register = updated_bhr

    # predict the outcome based on prediction counter
    def predict_outcome(self, counter):
        if counter >= 4:
            return "t"
        else:
            return "n"

    # write results to text file under output folder
    def write_results(self):
        file_op = open("output/gshare_output.txt", "w")
        file_op.write("COMMAND\n")
        file_op.write(
            f"./sim gshare {self.PC_bits} {self.bhr_bits} {self.trace_file}\n"
        )
        file_op.write("OUTPUT\n")
        file_op.write(f"number of predictions:		{self.predictions}\n")
        file_op.write(f"number of mispredictions:	{self.mispredictions}\n")
        file_op.write(
            f"misprediction rate:		{ self.mispredictions / self.predictions * 100:.2f}%\n"
        )
        file_op.write("FINAL GSHARE CONTENTS\n")
        for i in range(2**self.PC_bits):
            file_op.write(f"{i}\t{self.gshare_prediction_table[i]}\n")
        file_op.close()
