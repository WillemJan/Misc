#!/usr/bin/env bash

# # # # ## ### ## # #
#
# Update the baseurl for new files.
#
# http://wiki.dbpedia.org/dataset-categories/dbpedia-release
#
# # # # ## ### ## # #

DUMP_DATE="2015-04"
if [ ! -d "$DUMP_DATE/en/" ]; then
    mkdir -p "$DUMP_DATE/en/"
fi

BASEURL="http://downloads.dbpedia.org/$DUMP_DATE/core-i18n/en/"

dump_files="disambiguations_en.nt.bz2 infobox-properties_en.nt.bz2 labels_en.nt.bz2 long-abstracts_en.nt.bz2 redirects_en.nt.bz2 infobox-properties_en.nt.bz2 interlanguage-links_en.nt.bz2 labels_en.nt.bz2 long-abstracts_en.nt.bz2 page-links_en.nt.bz2 instance-types_en.nt.bz2"

for f in $dump_files;do
    cd "$DUMP_DATE/en"
    echo "Fetching $f from $BASEURL"
    wget -q "$BASEURL$f"
    echo "Done fetching $f, unpacking.."
    bunzip2 "$f"
    echo "Done unpacking $f"
    cd ../..
done
