rm(list=ls())
args <- commandArgs(trailingOnly=TRUE)
fileNames <- Sys.glob(paste(args[1]  ,"/*.csv", sep=''))

summary_output <- ""
for (fileName in fileNames) {
    runX <- read.csv(fileName)

    runX <- runX[-1, 2]
    summary_output <- paste( summary_output, summary(runX), sep='\n')
}

file_name <- paste(args[1], "/", args[2], "_summary.txt", sep='')
cat(summary_output,file=file_name,sep="\n",append=TRUE)
