rm(list=ls())

fileNames <- Sys.glob("mppref1.2/*.csv")

for (fileName in fileNames) {
    runX <- read.csv(fileName)

    runX <- runX[-1, ]
    print(summary(runX))
}
