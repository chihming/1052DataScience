#!/usr/bin/env Rscript

args = commandArgs(trailingOnly=TRUE)

input_filenames = c()
output_filename = c()
for (col in 1:length(args))
{
    if (args[col]=="-files")
    {
        if (col+1>length(args))
        {
            stop("please specify the [InputFileName]")
        }
        
        fnames = strsplit(args[col+1], ",")
        for (i in 1:length(fnames[[1]]))
        {
            fname = fnames[[1]][i]
            if(!file.exists(fname))
            {
                stop(fname, " not exists")
            }
            else
            {
                input_filenames = cbind(input_filenames, fname)
            }
        }
    }
    if (args[col]=="-out")
    {
        if (col+1>length(args))
        {
            stop("please specify the [OutputFileName]")
        }
        output_filename = args[col+1]
    }
}

if (length(input_filenames)==0)
{
    stop("please specify the [InputFileName]")
}

if (length(output_filename)==0)
{
    stop("please specify the [OutputFileName]")
}


#################################
### Main Process
#################################

if (file.exists(output_filename))
{
    file.remove(output_filename)
}

df = data.frame()
for (i in 1:length(input_filenames))
{

    TestCSV = read.csv(file=input_filenames[i])
    FI = gsub(".csv$", "", input_filenames[i])
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
    write.table(name_vec, append=T, row.names=F, col.names=F, sep=',', quote=F, file=output_filename)
    write.table(max_vec, append=T, row.names=F, col.names=F, sep=',', quote=F, file=output_filename)
}
