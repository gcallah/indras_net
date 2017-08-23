# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the mppref1.2 directory.

require(ggplot2)
require(reshape2)

rm(list=ls())

files <- list.files(path = "./mppref1.2", pattern ="(.+)csv")

filesWithPaths <- lapply(files, function(y) (paste("mppref1.2/", y, sep = "")))

filesWithPaths <- unlist(filesWithPaths)

dataSets <- lapply(filesWithPaths, read.csv)

result <- Reduce("+", dataSets) / length(dataSets)

print(result)
