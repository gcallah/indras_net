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

template = {}

def generate_wolfram_rules():
    with open("wolfram/wolfram_rules.txt","w+") as f: 
        for i in range(256):
            binary = bin(i + 256)[3:]
            for j in range(len(binary)):
                rule = str(rules[j])
                template[rule] = int(binary[j])
            f.write(str(template) + "\n")

    print("256 rules are successfully generated")
        
def read_wolfram_rules(file_name):
    rules_sets = []
    with open(file_name, "r") as f:
        all_rules = f.readlines()
        for i in all_rules:
            rules_sets.append(ast.literal_eval(i))

    return rules_sets
    
generate_wolfram_rules()
#print(read_wolfram_rules("wolfram_rules.txt"))
