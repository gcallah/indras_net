# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the mppref1.2 directory.

rm(list=ls())

args <- commandArgs(trailingOnly = TRUE)
csvDir <- args[1]

require(ggplot2)
require(reshape2)

files <- list.files(path = csvDir, pattern ="(.+)csv")
filesWithPaths <- unlist(lapply(files, function(y) (paste(csvDir, "/", y, sep = ""))))
dataSets <- lapply(filesWithPaths, read.csv)
dataSets <- lapply(dataSets, function(y) y[-1,])

# Get the average of the data sets.
average <- Reduce("+", dataSets) / length(dataSets)

# Add column for x-axis.
steps = as.numeric(rownames(average))
average[,"step"] <- steps

ggplot(melt(average, id.vars="step"), aes(step,value, col=variable)) + 
  geom_line()
