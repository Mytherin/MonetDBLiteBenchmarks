
acs_design <-
    update(
        
        acs_design ,
        
        relp = as.numeric( relp ) ,
        
        state_name =
            factor(
                as.numeric( st ) ,
                levels = 
                    c(1L, 2L, 4L, 5L, 6L, 8L, 9L, 10L, 
                    11L, 12L, 13L, 15L, 16L, 17L, 18L, 
                    19L, 20L, 21L, 22L, 23L, 24L, 25L, 
                    26L, 27L, 28L, 29L, 30L, 31L, 32L, 
                    33L, 34L, 35L, 36L, 37L, 38L, 39L, 
                    40L, 41L, 42L, 44L, 45L, 46L, 47L, 
                    48L, 49L, 50L, 51L, 53L, 54L, 55L, 
                    56L, 72L) ,
                labels =
                    c("Alabama", "Alaska", "Arizona", "Arkansas", "California", 
                    "Colorado", "Connecticut", "Delaware", "District of Columbia", 
                    "Florida", "Georgia", "Hawaii", "Idaho", "Illinois", "Indiana", 
                    "Iowa", "Kansas", "Kentucky", "Louisiana", "Maine", "Maryland", 
                    "Massachusetts", "Michigan", "Minnesota", "Mississippi", "Missouri", 
                    "Montana", "Nebraska", "Nevada", "New Hampshire", "New Jersey", 
                    "New Mexico", "New York", "North Carolina", "North Dakota", "Ohio", 
                    "Oklahoma", "Oregon", "Pennsylvania", "Rhode Island", "South Carolina", 
                    "South Dakota", "Tennessee", "Texas", "Utah", "Vermont", "Virginia", 
                    "Washington", "West Virginia", "Wisconsin", "Wyoming", "Puerto Rico")
            ) ,
        
        cit =
            factor( 
                cit , 
                levels = 1:5 , 
                labels = 
                    c( 
                        'born in the u.s.' ,
                        'born in the territories' ,
                        'born abroad to american parents' ,
                        'naturalized citizen' ,
                        'non-citizen'
                    )
            ) ,
        
        poverty_level = as.numeric( povpip ) ,
        
        married = as.numeric( mar %in% 1 ) ,
        
        sex = factor( sex , labels = c( 'male' , 'female' ) )
    )

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

# svyby( ~ sex , ~ cit , acs_design , svytotal )
# svyquantile( ~ poverty_level , acs_design , 0.5 , na.rm = TRUE )

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