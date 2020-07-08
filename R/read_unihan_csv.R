# Requires "python examples/csv_export.py" to be run

library(readr)
library(dplyr)

col_types = cols(
  glyph = col_character(),
  unicode = col_character(),
  kDefinition = col_character(),
  radical = col_integer(),
  additional_strokes = col_integer(),
  simplified_radical_indicator = col_logical(),
  is_kangxi_radical = col_logical(),
  simplified_glyph = col_character(),
  simplified_unicode = col_character(),
  traditional_glyph = col_character(),
  traditional_unicode = col_character(),
  variant_glyph = col_character(),
  variant_unicode = col_character(),
  kTotalStrokes = col_number(),
  kFrequency = col_integer(),
  kGradeLevel = col_integer(),
  kMandarin = col_character(),
  kHanyuPinlu = col_character(),
  kHanyuPinyin = col_character(),
  kCantonese = col_character(),
  kHangul = col_character(),
  kKorean = col_character(),
  kJapaneseKun = col_character(),
  kJapaneseOn = col_character(),
  kVietnamese = col_character(),
  kTang = col_character(),
  kTGHZ2013 = col_character(),
  kXHC1983 = col_character(),
  kRSAdobe_Japan1_6 = col_character(),
  kRSKangXi = col_character(),
  kRSUnicode = col_character(),
  kSemanticVariant = col_character(),
  kSimplifiedVariant = col_character(),
  kSpecializedSemanticVariant = col_character(),
  kSpoofingVariant = col_character(),
  kTraditionalVariant = col_character(),
  kZVariant = col_character(),
  kAccountingNumeric = col_integer(),
  kOtherNumeric = col_integer(),
  kPrimaryNumeric = col_number()
)


unihan <- read_delim(
  "data/unihan.csv",
  "\t",
  escape_double = FALSE,
  col_types = col_types,
  trim_ws = TRUE
)


radicals <- unihan %>% filter(is_kangxi_radical) %>% arrange(radical)

nrow(radicals)

View(radicals)
