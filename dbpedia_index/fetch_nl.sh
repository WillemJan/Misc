#!/usr/bin/env bash

#
# Update the baseurl for new files.
#
# http://wiki.dbpedia.org/dataset-categories/dbpedia-release
#

DUMP_DATE="current"
if [ ! -d "$DUMP_DATE" ]; then
    mkdir -p "$DUMP_DATE/nl/"
fi

BASEURL="http://downloads.dbpedia.org/$DUMP_DATE/core-i18n/nl/"
dump_files="disambiguations_nl.ttl.bz2 infobox-properties_nl.ttl.bz2 labels_en_uris_nl.ttl.bz2 long-abstracts-en-uris_nl.ttl.bz2 redirects_nl.ttl.bz2 infobox-properties-en-uris_nl.ttl.bz2 interlanguage_links_nl.ttl.bz2 labels_nl.ttl.bz2 long-abstracts_nl.ttl.bz2 page-links
_nl.ttl.bz2 instance-types_nl.ttl.bz2"
for f in $dump_files;do
    cd "$DUMP_DATE/nl"
    echo "Fetching $f from $BASEURL"
    wget -q "$BASEURL$f"
    echo "Done fetching $f, unpacking.."
    bunzip2 "$f"
    echo "Done unpacking $f"
    cd ../..
done


