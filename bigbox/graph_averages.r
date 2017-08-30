# Nathan Conroy
# Graphs the average amount of bigboxes, momandpops,
# and consumer utility in each .csv file in the directory
# specified in the first argument from the command line.

# Command to run:
# Rscript graph_averages.r <data_directory> <desired_output_filename>

packages <- c("ggplot2", "reshape")
if (length(setdiff(packages, rownames(installed.packages()))) > 0) {
  install.packages(setdiff(packages, rownames(installed.packages())),repos='http://cran.us.r-project.org')  
}

rm(list=ls())

args <- commandArgs(trailingOnly = TRUE)
csvDir <- args[1]

require(ggplot2)
require(reshape2)

files <- list.files(path = csvDir, pattern ="(.+)csv")
filesWithPaths <- unlist(lapply(files, function(y) (paste(csvDir, "/", y, sep = ""))))
dataSets <- lapply(filesWithPaths, read.csv)

# Get the average of the data sets.
average <- Reduce("+", dataSets) / length(dataSets)
print(average)
# Add column for x-axis.
steps = as.numeric(rownames(average))
average[,"step"] <- steps
average[,"Consumer.Utils"] <- average[,"Consumer.Utils"]
average <- average[-1,]

plot <- ggplot(melt(average, id.vars="step"), aes(step,value, col=variable)) + 
  geom_line()

ggsave(filename=args[2], plot=plot)
