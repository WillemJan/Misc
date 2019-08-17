#!/bin/bash

#java --dry-run -jar solr/server/start.jar -Dsolr.solr.home=/home/wfa010/code/create_dbpedia_index/solrhome/ -Djetty.port=4040

SOLR_PATH="/home/aloha/dbpedia_index/index/"

#rm -rf /mnt/ssd2/dbpedia3/data/

PORT="4041"
echo "Staring solr: $SOLR_PATH $PORT"
solr/bin/solr start -m 4g -f -p $PORT -Dsolr.solr.home=$SOLR_PATH

#solr/bin/solr start -f -p 4041 -Dsolr.solr.home=/home/wfa010/code/create_dbpedia_index/solrhome1/
