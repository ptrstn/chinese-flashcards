# Requires "python examples/csv_export.py" to be run

library(readr)
library(dplyr)
library(ggplot2)

col_types <- cols(
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
  hsk_level = col_integer(),
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
  kPrimaryNumeric = col_character()
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

first_grader <- unihan %>% filter(kGradeLevel == 1) %>% arrange(additional_strokes, radical)
nrow(first_grader)
View(first_grader)

unique(unihan$kGradeLevel)

hk_school_system <- unihan%>% filter(kGradeLevel >= 0)
hk_school_system$kGradeLevel <- as.factor(hk_school_system$kGradeLevel)
nrow(hk_school_system)
ggplot(hk_school_system, aes(factor(kGradeLevel), fill=factor(radical))) + geom_histogram(stat = "count") + theme(legend.position = "none")
ggplot(hk_school_system, aes(radical, colour=kGradeLevel)) + geom_freqpoly(stat="count")
ggplot(hk_school_system, aes(radical, colour = kGradeLevel)) + geom_density()
ggplot(hk_school_system, aes(radical, fill = kGradeLevel)) + geom_density(position = "stack")
ggplot(hk_school_system, aes(radical, fill = kGradeLevel)) + geom_density(position = "fill")
ggplot(hk_school_system, aes(radical, after_stat(count), fill = kGradeLevel)) + geom_density(position = "fill")

most_frequent <- unihan %>% filter(kFrequency == 1)%>% arrange(additional_strokes, radical)
nrow(most_frequent)
View(most_frequent)

numbers <- unihan %>% filter(!is.na(kPrimaryNumeric)) %>% arrange(as.numeric(kPrimaryNumeric))
nrow(numbers)
View(numbers)

accounting_numbers <- unihan %>% filter(!is.na(kAccountingNumeric)) %>% arrange(as.numeric(kAccountingNumeric))
nrow(accounting_numbers)
View(accounting_numbers)

other_numeric <- unihan %>% filter(!is.na(kOtherNumeric)) %>% arrange(as.numeric(kOtherNumeric))
nrow(other_numeric)
View(other_numeric)

radicals_summary <- unihan %>% 
  group_by(radical) %>%
  summarise(radical_count = n()) %>%
  arrange(desc(radical_count))

total_count <- sum(radicals_summary$radical_count)
radicals_summary$radical_count_perc <- radicals_summary$radical_count/total_count
radicals_summary$id <- seq.int(nrow(radicals_summary))
number_of_radicals <- max(radicals$radical)
radicals_summary$id_perc <- radicals_summary$id/number_of_radicals

ggplot(radicals_summary, aes(id, radical_count)) + geom_line()
ggplot(unihan, aes(radical)) + stat_ecdf(geom = "step")
ggplot(radicals_summary, aes(cumsum(radical_count_perc))) + stat_ecdf(geom = "step")
# => 25% of the radicals account to 75% of the total number of characters

ggplot(radicals_summary, aes(id, cumsum(radical_count_perc))) + geom_line()
# => 50 out of 214 Radicals make up 70% of all Unihan characters 

ggplot(radicals_summary, aes(cumsum(id_perc) , cumsum(radical_count_perc * 100))) + 
  geom_line() + 
  geom_hline(yintercept=80, linetype="dashed", color = "gray") +
  geom_vline(xintercept=10, linetype="dashed", color = "gray") +
  scale_x_continuous(breaks = c(0, 10, 25, 50, 75, 100)) + 
  scale_y_continuous(breaks = c(0, 25, 50, 75, 80, 100)) + 
  xlab("Proportion of the Number of Radicals in %") + 
  ylab("Coverage of the Total Number of Glyphs in %") +
  ggtitle("Cumulative Distribution of Radicals versus Total Number of Han Characters")

# => Effect here is even greater. See Pareto principle
# compare with https://www.researchgate.net/figure/Pareto-principle-Performing-20-of-the-effort-will-lead-to-80-of-the-results_fig3_37933519
