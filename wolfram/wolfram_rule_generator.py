#!/usr/bin/env python3
"""
A script to generate rules for Wolfram models.
"""
import ast

# states
B = 1
W = 0

rules = [
    (B, B, B),
    (B, B, W),
    (B, W, B),
    (B, W, W),
    (W, B, B),
    (W, B, W),
    (W, W, B),
    (W, W, W)
]

template = {
    (B, B, B): W,
    (B, B, W): W,
    (B, W, B): W,
    (B, W, W): B,
    (W, B, B): B,
    (W, B, W): B,
    (W, W, B): B,
    (W, W, W): W
}

def generate_wolfram_rules():
    f = open("wolfram_rules.txt","w+")
    for i in range(256):
        binary = bin(i + 256)[3:]
        for j in range(len(binary)):
            template[rules[j]] = int(binary[j])
        f.write(str(template) + "\n")
    f.close()
        
def read_wolfram_rules(file):
    rules_sets = []
    f = open(file,"r")
    all_rules = f.readlines()
    for i in all_rules:
        rules_sets.append(ast.literal_eval(i))
    f.close()
    return rules_sets
    
generate_wolfram_rules()
#print(read_wolfram_rules("wolfram_rules.txt"))