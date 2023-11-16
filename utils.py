"""
Module: utils.py
Author: Manikanta Varaganti
Date: November 18, 2023
Description: This module contains the utitlity functions.
"""


# converts given hexadecimal address to 32 bit binary address
def hex_to_bin(number):
    return bin(int(number, 16))[2:].zfill(32)
