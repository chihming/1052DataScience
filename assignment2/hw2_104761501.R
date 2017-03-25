list.of.packages <- c("ROCR")
new.packages <- list.of.packages[!(list.of.packages %in% installed.packages()[,"Package"])]
if(length(new.packages)) install.packages(new.packages, repos="http://cran.rstudio.com/")

library(ROCR)

eval_func<-function(query_m, name, pred, ref, score)
{

  if(query_m == "male"){
      
      T_IDX <- which(pred=="male")
      F_IDX <- which(pred=="female")
        
      TP <- length(which(ref[T_IDX]=="male"))
      FP <- length(which(ref[T_IDX]=="female"))
      TN <- length(which(ref[F_IDX]=="female"))
      FN <- length(which(ref[F_IDX]=="male"))
      
      sens <- round((TP/(TP+FN)), 2)
      spec <- round((TN/(TN+FP)), 2)
      f1 <- round((2*TP/(2*TP+FP+FN)), 2)
      
      ref_v <- as.numeric(ifelse(ref=="male", 1, 0))
      auc_pred <- prediction(predictions=score, labels=ref_v)
      auc_perf <- performance(auc_pred, "auc")
      auc_score <- round(as.numeric(auc_perf@y.values),2)

      return ( data.frame('method'=name, 'sensitivity'=sens, 'specificity'=spec, 'F1'=f1, 'AUC'=auc_score) )
}
  else if (query_m == "female") {
      
      score <- 1.0-score
      
      T_IDX <- which(pred=="female")
      F_IDX <- which(pred=="male")
        
      TP <- length(which(ref[T_IDX]=="female"))
      FP <- length(which(ref[T_IDX]=="male"))
      TN <- length(which(ref[F_IDX]=="male"))
      FN <- length(which(ref[F_IDX]=="female"))
      
      sens <- round((TP/(TP+FN)), 2)
      spec <- round((TN/(TN+FP)), 2)
      f1 <- round((2*TP/(2*TP+FP+FN)), 2)
      
      ref_v <- as.numeric(ifelse(ref=="female", 1, 0))
      auc_pred <- prediction(predictions=score, labels=ref_v)
      auc_perf <- performance(auc_pred, "auc")
      auc_score <- round(as.numeric(auc_perf@y.values),2)

      return ( data.frame('method'=name, 'sensitivity'=sens, 'specificity'=spec, 'F1'=f1, 'AUC'=auc_score) )

  } else {
    stop(paste("ERROR: unknown query function", query_m))
  }

}

# read parameters
args = commandArgs(trailingOnly=TRUE)
if (length(args)==0) {
  stop("USAGE: Rscript hw2_104761501.R --target male/female --files file1 file2 ... filen --out result.csv", call.=FALSE)
}

# parse parameters
i<-1 
while(i < length(args))
{
  if(args[i] == "--target"){
    query_m<-args[i+1]
    i<-i+1
  }else if(args[i] == "--files"){
    j<-grep("-", c(args[(i+1):length(args)], "-"))[1]
    files<-args[(i+1):(i+j-1)]
    i<-i+j-1
  }else if(args[i] == "--out"){
    out_f<-args[i+1]
    i<-i+1
  }else{
    stop(paste("Unknown flag", args[i]), call.=FALSE)
  }
  i<-i+1
}

print("PROCESS")
print(paste("query mode :", query_m))
print(paste("output file:", out_f))
print(paste("files      :", files))

# read files
rows <- data.frame()
for(file in files)
{
  name<-gsub(".csv", "", basename(file))
  d<-read.table(file, header=T,sep=",")
  eval_res <- eval_func(query_m, name, d$prediction, d$reference, d$pred.score)
  rows <- rbind(rows, eval_res)
}

top_sens <- rows[ which.max(rows$sensitivity), ]$method
top_spec <- rows[ which.max(rows$specificity), ]$method
top_f1 <- rows[ which.max(rows$F1), ]$method
top_auc <- rows[ which.max(rows$AUC), ]$method
rows <- rbind(rows, (data.frame("method"="highest", "sensitivity"=top_sens, "specificity"=top_spec, "F1"=top_f1, "AUC"=top_auc)))

print (rows)

write.table(rows, file=out_f, row.names = F, quote = F, sep=',')
