library("ggplot2")
options("width"=200)
pos <- read.delim('data/test_data', sep=" ", stringsAsFactor=FALSE, header=FALSE)
names(pos) <- c("positie", "woord", "lemma", "mutaties", "type1", "getal", "ner", "type_woord", "getal1", "dunno")
pos$positie <- NULL
normalize.pos <- function(l) {
    split.pos <- tryCatch(strsplit(l, "-")[[1]], error= function(e) return (NA))
    if (length(split.pos) >= 2) {
        return (split.pos[2])
    } else {
        return (split.pos)
    }
}
normalize.type <- function(l) {
    split.pos <- tryCatch(strsplit(l, "\\(")[[1]], error= function(e) return (NA))
    if (length(split.pos) >= 2) {
        return (split.pos[1])
    } else {
        return (split.pos)
    }
}
pos$type_woord <- lapply(pos$type_woord, normalize.pos)
pos$type1 <- lapply(pos$type1, normalize.type)
print("Gemiddelde gebruik per type:")
gem_list = list()
name_list = list()
for (item in unique(unlist(pos$type1))) {
    cat(item, " : ", mean(unlist(pos$type1) == item) * 100, "\n")
    #cat(count(unlist(pos$type1), item))
    gem_list <- c(gem_list, mean(unlist(pos$type1) == item) * 100)
    name_list <- c(name_list, item)
}

print("Frequentie gebruik per type:")
print(table(unlist(pos$type1)))
abs_list <- unlist(as.data.frame(table(unlist(pos$type_woord)))[["Freq"]])
barplot(table(unlist(pos$type_woord)), col=c("darkblue"))
