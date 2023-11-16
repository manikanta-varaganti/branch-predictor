"""
Module: sim.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module provides the simulation of Smith n-bit, Bimodal, Gshare and Hybrid branch predictors.
"""
import sys
from smith import SmithPredictor
from bimodal import BimodalPredictor
from gshare import GSharePredictor
from hybrid import HybridPredcitor


if __name__ == "__main__":
    predictor = sys.argv[1]

    if predictor == "smith":
        sp = SmithPredictor(sys.argv[2], sys.argv[3])
        sp.predict()
        sp.write_results()
    elif predictor == "bimodal":
        bp = BimodalPredictor(sys.argv[2], sys.argv[3])
        bp.predict()
        bp.write_results()
    elif predictor == "gshare":
        gp = GSharePredictor(sys.argv[2], sys.argv[3], sys.argv[4])
        gp.predict()
        gp.write_results()
    elif predictor == "hybrid":
        hp = HybridPredcitor(
            sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6]
        )
        hp.predict()
        hp.write_results()
    else:
        print("Enter a valid predictor")
