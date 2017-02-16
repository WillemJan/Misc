
Project : 

    KB thesauri matching to DBpedia.

Prerequisites : 

    - SOLR installed on Tomcat (http://wiki.apache.org/solr/SolrTomcat) 
        (For indexing the KB thesauri data)
    - MongoDB 
        (For storing the links between the two collections)

Process : 

    step 1: copy the config file sorl.xml to tomcat6 (cp ./solr_config/solr.xml /etc/tomcat6/Caltalina)
    step 2: configure SOLR to accept thesauri data (mkdir /etc/solr; cp -rav ./solr_config/ggc-thes /etc/solr/; mkdir -p /opt/data/ggc-thes)
    step 3: restart tomcat6 (/etc/init.d/tomcat6 restart)
    
    * At this point, your solr endpoint must be available at http://localhost:8080/solr/ggc-thes/select/?q=*:*

    step 4: load the example data into your solr endpoint. (./kb_thesauri_to_solr.py)

    * At this point, your MongoDB must be available at localhost (mongo localhost)

    step 5: run the example (./map_dbpedia_to_kb_thesauri)

    * At this point, the links to the thesauri are stored in MongoDB database_name: expand collection_name : ggc-thes
