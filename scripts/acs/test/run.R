

sum( weights( acs_design , "sampling" ) != 0 )


svyby( ~ one , ~ cit , acs_design , unwtd.count )
svytotal( ~ one , acs_design )

svyby( ~ one , ~ cit , acs_design , svytotal )
svymean( ~ poverty_level , acs_design , na.rm = TRUE )

svyby( ~ poverty_level , ~ cit , acs_design , svymean , na.rm = TRUE )
svymean( ~ sex , acs_design )

svyby( ~ sex , ~ cit , acs_design , svymean )
svytotal( ~ poverty_level , acs_design , na.rm = TRUE )

svyby( ~ poverty_level , ~ cit , acs_design , svytotal , na.rm = TRUE )
svytotal( ~ sex , acs_design )

# svyby( 
#     ~ poverty_level , 
#     ~ cit , 
#     acs_design , 
#     svyquantile , 
#     0.5 ,
#     ci = TRUE ,
#     keep.var = TRUE ,
#     na.rm = TRUE
# )

# svyratio( 
#     numerator = ~ ssip , 
#     denominator = ~ pincp , 
#     acs_design ,
#     na.rm = TRUE
# )

# sub_acs_design <- subset( acs_design , agep >= 65 )

# svymean( ~ poverty_level , sub_acs_design , na.rm = TRUE )

# this_result <- svymean( ~ poverty_level , acs_design , na.rm = TRUE )

# coef( this_result )
# SE( this_result )
# confint( this_result )
# cv( this_result )

# grouped_result <-
#     svyby( 
#         ~ poverty_level , 
#         ~ cit , 
#         acs_design , 
#         svymean ,
#         na.rm = TRUE 
#     )
    
# coef( grouped_result )
# SE( grouped_result )
# confint( grouped_result )
# cv( grouped_result )

# degf( acs_design )

# svyvar( ~ poverty_level , acs_design , na.rm = TRUE )

# # SRS without replacement
# svymean( ~ poverty_level , acs_design , na.rm = TRUE , deff = TRUE )

# # SRS with replacement
# svymean( ~ poverty_level , acs_design , na.rm = TRUE , deff = "replace" )

# svyciprop( ~ married , acs_design ,
#     method = "likelihood" )


# svyby( ~ sex , ~ cit , acs_design , svytotal )
# svyquantile( ~ poverty_level , acs_design , 0.5 , na.rm = TRUE )

# svyttest( poverty_level ~ married , acs_design )

# svychisq( 
#     ~ married + sex , 
#     acs_design 
# )
# glm_result <- 
#     svyglm( 
#         poverty_level ~ married + sex , 
#         acs_design 
#     )

# summary( glm_result )



# library(convey)
# acs_design <- convey_prep( acs_design )

# svygini( ~ hincp , acs_design , na.rm = TRUE )


# pums_estimate <- 
#     c( 285681 , 314701 , 300814 , 334318 , 327896 , 629329 , 599719 , 644212 , 
#     342205 , 300254 , 464893 , 231293 , 87985 )

# pums_standard_error <- 
#     c( 2888 , 5168 , 5009 , 3673 , 3521 , 4825 , 4088 , 
#     4398 , 5329 , 5389 , 1938 , 3214 , 2950 )

# pums_margin_of_error <- 
#     c( 4751 , 8501 , 8240 , 6043 , 5792 , 7937 , 6725 , 
#     7234 , 8767 , 8865 , 3188 , 5287 , 4853 )

# results <-
#     svytotal( 
#         ~ as.numeric( agep %in% 0:4 ) +
#         as.numeric( agep %in% 5:9 ) +
#         as.numeric( agep %in% 10:14 ) +
#         as.numeric( agep %in% 15:19 ) +
#         as.numeric( agep %in% 20:24 ) +
#         as.numeric( agep %in% 25:34 ) +
#         as.numeric( agep %in% 35:44 ) +
#         as.numeric( agep %in% 45:54 ) +
#         as.numeric( agep %in% 55:59 ) +
#         as.numeric( agep %in% 60:64 ) +
#         as.numeric( agep %in% 65:74 ) +
#         as.numeric( agep %in% 75:84 ) +
#         as.numeric( agep %in% 85:100 ) , 
#         acs_design
#     )

