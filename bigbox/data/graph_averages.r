# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the mppref1.2 directory.

require(ggplot2)
require(reshape2)

rm(list=ls())

files <- list.files(path = "./mppref1.2", pattern ="(.+)csv")
filesWithPaths <- unlist(lapply(files, function(y) (paste("mppref1.2/", y, sep = ""))))
dataSets <- lapply(filesWithPaths, read.csv)

# Get the average of the data sets.
average <- Reduce("+", dataSets) / length(dataSets)

# Add column for x-axis.
steps = as.numeric(rownames(average))
average[,"step"] <- steps

ggplot(melt(average, id.vars="step"), aes(step,value, col=variable)) + 
  geom_line()
