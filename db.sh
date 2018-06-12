#!/bin/bash
# This script bth stages django db changes, and commits them.
./stage.sh $1
./commit.sh
