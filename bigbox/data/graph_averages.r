# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the mppref1.2 directory.

require(ggplot2)
require(reshape2)

rm(list=ls())

files <- list.files(path = "./mppref1.2", pattern ="(.+)csv")

filesWithPaths <- unlist(lapply(files, function(y) (paste("mppref1.2/", y, sep = ""))))

dataSets <- lapply(filesWithPaths, read.csv)

average <- Reduce("+", dataSets) / length(dataSets)

print(average)

steps = as.numeric(rownames(average))

average[,"step"] <- steps

print(average)

average <- melt(average, id.vars="step")

ggplot(average, aes(step,value, col=variable)) + 
  geom_line()
