library(dplyr)
library(ggplot2)
library(ggthemes)
library(ggrepel)
library(stringr)
library(grid)
library(reshape2)


theme <- theme_few(base_size = 24) + 
theme(axis.title.y=element_text(vjust=0.9), 
  axis.title.x=element_text(vjust=-0.1),
  axis.ticks.x=element_blank(),
  text=element_text(family="serif"),
  legend.position="none")




data <- read.table("temp_data.csv", header=T,  sep=",", stringsAsFactors=F, na.strings="-1")

data$time[data$time < 10] <- round(data$time[data$time < 10], 2)
data$time[data$time >= 10] <- round(data$time[data$time >= 10], 1)

ymax <- as.integer(Sys.getenv('Y_MAX_BOUND'))

pdf(Sys.getenv('PLOT_NAME'), width=8, height=6)
ggplot(data, aes(x = reorder(system, time), y = time, fill = system, label=time)) + geom_bar(stat = "identity", width=.7) + theme + xlab("") + ylab("Wall clock time (s)") + scale_y_continuous(limits=c(0, ymax)) + geom_text(size=7, vjust=-.3, family="serif")
dev.off()
