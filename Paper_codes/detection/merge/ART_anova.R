library(ARTool)
setwd("/Users/yiqinpan/OneDrive - University of Florida/research/Linear Detection/codes/detection/merge")
types = c( 'false_posi_item', 'false_posi_ppl','false_neg_item', 'false_neg_ppl', 'precision_item', 'precision_ppl')
for (ele in types){
  data = read.csv(file = paste('result_mid/',ele,".csv",sep = ""),header = FALSE)[,c(4,5,6,7,8,9)]
  #colnames(data)=c("ewp_rate", "ci_rate", "iterat_times", "ab_cri", "val")
  colnames(data)=c("ewp_rate", "ci_rate", "simu_distr", "ci_access", "iterat_times",  "val")
  data = data.frame(data)
  data$ewp_rate = factor(data$ewp_rate) 
  data$ci_rate = factor(data$ci_rate) 
  data$simu_distr = factor(data$simu_distr) 
  data$ci_access = factor(data$ci_access) 
  data$iterat_times = factor(data$iterat_times) 
  
  data=data[which( data$ewp_rate!=0 & (data$iterat_times==30 | data$iterat_times==60)),]
  
  model = art(val ~ ewp_rate, data = data)
  #model = art(val ~ ewp_rate*ci_rate*simu_distr*ci_access*iterat_times, data = data)
  #print(model)
  Result = anova(model)
  Result$part.eta.sq = with(Result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
  #print(ele)
  #print(Result)
  write.table(Result, file =  paste('anova/',ele,".csv",sep = ""),sep = ",", append = TRUE)
  
  model = art(val ~ ci_rate, data = data)
  #model = art(val ~ ewp_rate*ci_rate*simu_distr*ci_access*iterat_times, data = data)
  #print(model)
  Result = anova(model)
  Result$part.eta.sq = with(Result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
  #print(ele)
  #print(Result)
  write.table(Result, file =  paste('anova/',ele,".csv",sep = ""),sep = ",", row.names=FALSE, col.names=FALSE,append = TRUE)
  
  
  model = art(val ~ simu_distr, data = data)
  #model = art(val ~ ewp_rate*ci_rate*simu_distr*ci_access*iterat_times, data = data)
  #print(model)
  Result = anova(model)
  Result$part.eta.sq = with(Result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
  #print(ele)
  #print(Result)
  write.table(Result, file =  paste('anova/',ele,".csv",sep = ""),sep = ",", row.names=FALSE, col.names=FALSE,append = TRUE)
  
  
  model = art(val ~ ci_access, data = data)
  #model = art(val ~ ewp_rate*ci_rate*simu_distr*ci_access*iterat_times, data = data)
  #print(model)
  Result = anova(model)
  Result$part.eta.sq = with(Result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
  #print(ele)
  #print(Result)
  write.table(Result, file =  paste('anova/',ele,".csv",sep = ""),sep = ",", row.names=FALSE, col.names=FALSE,append = TRUE)
  
  
  model = art(val ~ iterat_times, data = data)
  #model = art(val ~ ewp_rate*ci_rate*simu_distr*ci_access*iterat_times, data = data)
  #print(model)
  Result = anova(model)
  Result$part.eta.sq = with(Result, `Sum Sq`/(`Sum Sq` + `Sum Sq.res`))
  #print(ele)
  #print(Result)
  write.table(Result, file =  paste('anova/',ele,".csv",sep = ""),sep = ",", row.names=FALSE, col.names=FALSE,append = TRUE)
  


}




for (ele in types){
  data = read.csv(file = paste('result_mid/',ele,".csv",sep = ""),header = FALSE)[,c(4,5,6,7,8,9)]
  #colnames(data)=c("ewp_rate", "ci_rate", "iterat_times", "ab_cri", "val")
  colnames(data)=c("ewp_rate", "ci_rate", "simu_distr", "ci_access", "iterat_times",  "val")
  data = data.frame(data)
  data$ewp_rate = factor(data$ewp_rate) 
  data$ci_rate = factor(data$ci_rate) 
  data$simu_distr = factor(data$simu_distr) 
  data$ci_access = factor(data$ci_access) 
  data$iterat_times = factor(data$iterat_times) 
  
  data=data[which( data$ewp_rate!=0 & (data$iterat_times==30 | data$iterat_times==60)),]
  print(bartlett.test(val ~ ewp_rate,data=data))
  print(bartlett.test(val ~ ci_rate,data=data))
  print(bartlett.test(val ~ simu_distr,data=data))
  print(bartlett.test(val ~ ci_access,data=data))
  print(bartlett.test(val ~ iterat_times,data=data))
  
}
#bartlett.test(val ~ ewp_rate,data=data)
#shapiro.test(data$val)
