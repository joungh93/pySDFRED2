start_time <- Sys.time()


# ----- Libraries ----- #
library(FITSio)
library(readr)


# ----- Initial declarations ----- #
dir_Raw <- file.path(getwd(), "Raw")
imglist <- list.files(dir_Raw)
n_img <- length(imglist)

col <- c("EXP-ID", "FRAMEID", "DATE-OBS", "DATA-TYP", "OBJECT" ,"FILTER01", "EXPTIME")
n_col <- length(col)
eval(parse(text = paste0("v0", 1:n_col, " <- NULL")))


# ----- Reading headers of raw images ----- #
for (i in seq(n_img)) {
  message <- sprintf("Reading images: %d/%d", i, n_img)
  print(message)
  
  dh <- readFITS(file.path(dir_Raw, imglist[i]))
  for (j in seq(n_col)) {
    idx <- which(dh$hdr == col[j])
    if (length(idx) > 1) {
      idx <- idx[idx %% 2 == 1]
    }
    eval(parse(text = sprintf("v%02d <- c(v%02d, dh$hdr[idx+1])", j, j)))
  }
}


# ----- Saving the results to data frame ----- #
vv <- paste(paste("v0", 1:n_col, sep=""), collapse=", ")
eval(parse(text = paste("df <- data.frame(", vv, ")", sep="")))
names(df) <- col
write_csv(df, "raw_info.csv")


# ----- Printing the running time ----- #
end_time <- Sys.time()
print(sprintf("--- Running time: %.4f min ---", end_time - start_time))

