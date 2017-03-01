#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

if (length(args)!=4 | args[1]!="-files" | args[3]!="-out") {
    stop("Please follow the command:\n
    \"hw1_104761501.R -files [InputFileName] -out [OutputFileName]\"", call.=FALSE)
}

TestCSV = read.csv(file=args[2])
FI = args[2]
FI = gsub(".csv$", "", FI)
name_vec = c('set')
max_vec = c(FI)

for (col in 1:length(TestCSV))
{
    if (class(TestCSV[,col])=="numeric")
    {
        name_vec = cbind(name_vec, names(TestCSV[col]))
        max_vec = cbind(max_vec, round(max(TestCSV[,col]), digits=2))
    }
}
df = data.frame()
df = rbind(df, max_vec)
colnames(df) = name_vec

write.table(df, row.names=FALSE, col.names=TRUE, sep=',', quote=FALSE, file=args[4])

