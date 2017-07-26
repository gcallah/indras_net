rm(list=ls())

run.1 <- read.csv("mppref1.2/run1.csv")

run.1 <- run.1[-1, ]
summary(run.1)
