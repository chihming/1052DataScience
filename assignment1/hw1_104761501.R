#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

if (length(args)!=4 | args[1]!="-files" | args[3]!="-out") {
    stop("Please follow the command:\n
    \"hw1_104761501.R -files [InputFileName] -out [OutputFileName]\"", call.=FALSE)
}

TestCSV = read.csv(file=args[2])
FI = args[2]
FI = gsub(".csv$", "", FI)
MW = round(max(TestCSV[,'weight']), digits=2)
MH = round(max(TestCSV[,'height']), digits=2)

df = data.frame(FI, MW, MH)
colnames(df) = c("set", "weight", "height")

write.table(df, row.names=FALSE, col.names=TRUE, sep=',', quote=FALSE, file=args[4])

