library(readr)
library(dplyr)
library(tidyr)
library(stringr)
library(stringi)

files <- list.files(path = "data/unihan", pattern = "*.txt", full.names = TRUE)


read_unihan_file <- function(file_path){
  read_delim(
    file_path,
    "\t",
    escape_double = FALSE,
    col_names = c("unicode", "field", "description"),
    col_types = cols(
      unicode = col_character(),
      field = col_character(),
      description = col_character()
    ),
    comment = "#",
    trim_ws = TRUE
  )
}

data <- bind_rows(
  read_unihan_file("data/unihan/Unihan_DictionaryIndices.txt"),
  read_unihan_file("data/unihan/Unihan_DictionaryLikeData.txt"),
  read_unihan_file("data/unihan/Unihan_IRGSources.txt"),
  read_unihan_file("data/unihan/Unihan_NumericValues.txt"),
  read_unihan_file("data/unihan/Unihan_OtherMappings.txt"),
  read_unihan_file("data/unihan/Unihan_RadicalStrokeCounts.txt"),
  read_unihan_file("data/unihan/Unihan_Readings.txt"),
  read_unihan_file("data/unihan/Unihan_Variants.txt"),
)
