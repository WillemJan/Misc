ate=`date +%m-%d-%Y`

if [ -e "$ate"_dump.xml.gz ];then
    echo 'data is here'
else
    echo 'getting jamendo data'
    curl -s http://img.jamendo.com/data/dbdump_artistalbumtrack.xml.gz > "$ate"_dump.xml.gz

    echo 'converting jamendo data to solr artists'
    zcat "$ate"_dump.xml.gz | xalan -xsl artist.xsl -out new.xml
    URL="http://localhost:8080/solr/jamendo1_artists/update"

    echo 'posting artist data'
    curl $URL --data-binary @new.xml -H 'Content-type:application/xml' 
    curl $URL --data-binary '<commit/>' -H 'Content-type:application/xml'
fi

echo 'artists diffs'
URL="http://localhost:8080/solr/jamendo1_artists/terms/?terms.fl=id_int&terms=true&terms.limit=-1"
curl -s $URL | xmllint --format - > out1.xml
URL="http://localhost:8080/solr/jamendo_artists/terms/?terms.fl=id_int&terms=true&terms.limit=-1"
curl -s $URL | xmllint --format - > out.xml

diff out.xml out1.xml > new_and_old.diff
