# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the mppref1.2 directory.

require(ggplot2)
require(reshape2)

rm(list=ls())

x <- list.files(path = "./mppref1.2", pattern ="(.+)csv")

print(x)

x <- lapply(x, function(y) (paste("mppref1.2/", y, sep = "")))

print(x)

x <- unlist(x)

print(x)

x <- lapply(x, read.csv)

x <- Reduce("+", x) / length(x)

print(x)
