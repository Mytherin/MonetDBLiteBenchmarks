
DBI::dbWriteTable(con, "acs_df", acs_df)

acs_design_stored <-
    svrepdesign(
        weight = ~pwgtp ,
        repweights = 'pwgtp[0-9]+' ,
        scale = 4 / 80 ,
        rscales = rep( 1 , 80 ) ,
        mse = TRUE ,
        type = 'JK1' ,
        data = "acs_df",
        dbtype = dbtype,
        dbname = database
    )

acs_design <-
    update(
        
        acs_design_stored ,
        
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

