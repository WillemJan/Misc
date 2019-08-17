curl -XGET 'http://localhost:9200/dbpedia/_termvectors?pretty=true' -d '{
  "fields" : ["text", "some_field_without_term_vectors"],
    "offsets" : true,
      "positions" : true,
        "term_statistics" : true,
          "field_statistics" : true
      }'
