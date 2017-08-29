#!/bin/bash

BOX_DIR="bigbox"
MODEL="$BOX_DIR.big_box_run"
DATA_DIR="$BOX_DIR/tmp"
PREFS="prefs.json"
NUM_RUNS=75
PERIODS=75

echo $DATA_DIR

OUT_DIR="$DATA_DIR/mppref1.0"
./runs.sh $NUM_RUNS $MODEL "$OUT_DIR/$PREFS" "$OUT_DIR/run" $PERIODS
Rscript "$BOX_DIR/graph_averages.r" "$OUT_DIR" "$OUT_DIR/plot_mppref1.0.pdf"
OUT_DIR="$DATA_DIR/mppref1.2"
./runs.sh $NUM_RUNS $MODEL "$OUT_DIR/$PREFS" "$OUT_DIR/run" $PERIODS
Rscript "$BOX_DIR/graph_averages.r" "$OUT_DIR" "$OUT_DIR/plot_mppref1.2.pdf"
OUT_DIR="$DATA_DIR/mppref1.4"
./runs.sh $NUM_RUNS $MODEL "$OUT_DIR/$PREFS" "$OUT_DIR/run" $PERIODS
Rscript "$BOX_DIR/graph_averages.r" "$OUT_DIR" "$OUT_DIR/plot_mppref1.4.pdf"
OUT_DIR="$DATA_DIR/mppref1.6"
./runs.sh $NUM_RUNS $MODEL "$OUT_DIR/$PREFS" "$OUT_DIR/run" $PERIODS
Rscript "$BOX_DIR/graph_averages.r" "$OUT_DIR" "$OUT_DIR/plot_mppref1.6.pdf"
OUT_DIR="$DATA_DIR/mppref1.8"
./runs.sh $NUM_RUNS $MODEL "$OUT_DIR/$PREFS" "$OUT_DIR/run" $PERIODS
Rscript "$BOX_DIR/graph_averages.r" "$OUT_DIR" "$OUT_DIR/plot_mppref1.8.pdf"
