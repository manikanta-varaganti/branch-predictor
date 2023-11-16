"""
Module: hybrid.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module contains the simulator logic for hybrid branch predictor that uses both bimodal and gshare predictors.
"""
import sys
from utils import *
from gshare import GSharePredictor
from bimodal import BimodalPredictor


class HybridPredcitor:
    def __init__(self, choser_bits, gshare_bits, bhr_bits, bimodal_bits, trace_file):
        self.predictions = 0
        self.mispredictions = 0
        self.choser_bits = int(choser_bits)
        self.gshare_bits = int(gshare_bits)
        self.bhr_bits = int(bhr_bits)
        self.bimodal_bits = int(bimodal_bits)
        self.trace_file = trace_file

        self.gshare_predictor = GSharePredictor(
            self.gshare_bits, self.bhr_bits, self.trace_file
        )
        self.bimodal_predictor = BimodalPredictor(self.bimodal_bits, self.trace_file)
        self.choser_prediction_table_size = 2**self.choser_bits
        self.choser_prediction_table = [
            1
        ] * self.choser_prediction_table_size  # initialize the choser table

    # returns the index value for choser table
    def get_index(self, address):
        binary_address = hex_to_bin(address)[
            -2 - self.choser_bits : -2
        ]  # obtain the last k bit address by discarding the lowest 2 bits
        return int(binary_address, 2)

    # returns the prediction using a GShare predictor
    def get_gshare_prediction(self, address):
        index = self.gshare_predictor.get_index(address)
        pred_counter = self.gshare_predictor.gshare_prediction_table[index]
        pred_outcome = self.gshare_predictor.predict_outcome(pred_counter)
        return pred_outcome

    # returns the prediction using a Bimodal predictor
    def get_bimodal_prediction(self, address):
        index = self.bimodal_predictor.get_index(address)
        pred_counter = self.bimodal_predictor.bimodal_prediction_table[index]
        pred_outcome = self.bimodal_predictor.predict_outcome(pred_counter)
        return pred_outcome

    # hybrid branch predictor logic
    def predict(self):
        with open("traces/" + self.trace_file, "r") as file:
            traces = file.readlines()
            for instruction in traces:
                address, outcome = instruction.split(" ")
                actual_outcome = outcome.strip()
                self.predictions += 1

                # get the index values of choser, bimodal and gshare prediction tables
                choser_index = self.get_index(address)
                bimodal_index = self.bimodal_predictor.get_index(address)
                gshare_index = self.gshare_predictor.get_index(address)

                # obtain the gshare and bimodal predictions
                gshare_prediction = self.get_gshare_prediction(address)
                bimodal_prediction = self.get_bimodal_prediction(address)

                # select the approporaite predictor based on counter
                if self.choser_prediction_table[choser_index] >= 2:
                    prediction_outcome = gshare_prediction  # GShare brnach predictor
                    self.gshare_predictor.update_counter(actual_outcome, gshare_index)
                    if prediction_outcome != actual_outcome:
                        self.mispredictions += 1
                else:
                    prediction_outcome = bimodal_prediction  # Bimodal branch predictor
                    self.bimodal_predictor.update_counter(actual_outcome, bimodal_index)
                    if prediction_outcome != actual_outcome:
                        self.mispredictions += 1

                # update the Gshare's branch history register
                if actual_outcome == "t":
                    self.gshare_predictor.update_bhr("1")
                else:
                    self.gshare_predictor.update_bhr("0")

                # update the choser counter
                if (
                    actual_outcome == gshare_prediction
                    and actual_outcome != bimodal_prediction
                ):
                    counter = self.choser_prediction_table[choser_index] + 1
                    self.choser_prediction_table[choser_index] = min(3, counter)
                elif (
                    actual_outcome == bimodal_prediction
                    and actual_outcome != gshare_prediction
                ):
                    counter = self.choser_prediction_table[choser_index] - 1
                    self.choser_prediction_table[choser_index] = max(0, counter)
                else:
                    None

    # write results to text file under output folder
    def write_results(self):
        file_op = open("output/hybrid_output.txt", "w")
        file_op.write("COMMAND\n")
        file_op.write(
            f"./sim hybrid {self.choser_bits} {self.gshare_bits} {self.bhr_bits} {self.bimodal_bits} {self.trace_file}\n"
        )
        file_op.write("OUTPUT\n")
        file_op.write(f"number of predictions:		{self.predictions}\n")
        file_op.write(f"number of mispredictions:	{self.mispredictions}\n")
        file_op.write(
            f"misprediction rate:		{ self.mispredictions / self.predictions * 100:.2f}%\n"
        )
        file_op.write("FINAL CHOOSER CONTENTS\n")
        for i in range(self.choser_prediction_table_size):
            file_op.write(f"{i}\t{self.choser_prediction_table[i]}\n")

        file_op.write("FINAL GSHARE CONTENTS\n")
        for i in range(self.gshare_predictor.gshare_prediction_table_size):
            file_op.write(f"{i}\t{self.gshare_predictor.gshare_prediction_table[i]}\n")

        file_op.write("FINAL BIMODAL CONTENTS\n")
        for i in range(self.bimodal_predictor.bimodal_prediction_table_size):
            file_op.write(
                f"{i}\t{self.bimodal_predictor.bimodal_prediction_table[i]}\n"
            )
