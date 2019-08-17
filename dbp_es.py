#ElasticSearch helpers.
from elasticsearch import Elasticsearch

def es_create_index(delete_first=True):
    with open(ES_MAPPING, 'r') as fh:
        mapping = fh.read()

    if delete_first:
        try:
            response = ES.indices.delete(index=ES_INDEX_NAME)
        except:
            pass

    response = ES.indices.create(index=ES_INDEX_NAME,
                                 ignore=400,
                                 body=mapping)


def es_worker(q, i, type_op):
    errors = 0
    done = False

    docs = []
    bulk_data = []

    while True:
        for i in range(int(COMMIT_MAX / ES_THREADS)):
            if q.not_empty:
                try:
                    doc = q.get_nowait()
                    q.task_done()
                except:
                    doc = False
                if doc:
                    docs.append(doc)

        if not docs:
            time.sleep(0.01)

        for doc in docs:
            if type_op == "index":
                op_dict = {"index": {"_index": ES_INDEX_NAME,
                                     "_type": ES_INDEX_NAME,
                                     "_id": doc.get('id')}}
            elif type_op == "update":
                op_dict = {"update": {"_index": ES_INDEX_NAME,
                                      "_type": ES_INDEX_NAME,
                                      "_id": doc.get('id')}}

            bulk_data.append(op_dict)
            bulk_data.append(doc)

        if docs:
            done = False
            while not done:
                try:
                    res = ES.bulk(index=ES_INDEX_NAME,
                                  body=bulk_data,
                                  refresh=False)

                    if res.get('errors') == False:
                        done = True
                        print("Committed: %i" % len(docs))
                    else:
                        errors += 1
                        print("ERROR1", errors, res)
                        time.sleep(1)
                except:
                    errors += 1
                    e = sys.exc_info()[0]
                    print("ERROR2", errors, e)
                    time.sleep(1)
    return


def es_lookup(label, value):
    res = ES.search(index=ES_INDEX_NAME,
                    q='%s:"%s"' % ('id_nl', value))

    if not res.get('hits').get('total') == 1:
        return False

    return res.get('hits').get('hits')[0].get('_source')


class es_worker_lookup(threading.Thread):
    def __init__(self, que):
        threading.Thread.__init__(self)
        self.event = event = threading.Event()
        self.q = que

    def run(self):
        errors = 0
        done = False

        docs = []
        bulk_data = []

        while not self.event.is_set():
            for i in range(int(COMMIT_MAX / ES_THREADS)):
                if self.q.not_empty:

                    try:
                        doc = self.q.get_nowait()
                        self.q.task_done()
                    except:
                        doc = False

                    if doc:
                        docs.append(doc)

            for doc in docs:
                current_doc = es_lookup("label_nl", doc.get('id_nl'))

                if current_doc:
                    for item in current_doc:
                        print(type(item), current_doc.get('id_nl'))
                        if isinstance(item, list):
                            [doc[item].append(i) for i in current_doc.get(i) if not i in doc[item]]
                            pint("APPEND ACTION!!")

                    doc['id'] = current_doc.get('id')

                    op_dict = {"update": {"_index": ES_INDEX_NAME,
                                          "_type": ES_INDEX_NAME,
                                          "_id": doc.get('id')}}

                    bulk_data.append(op_dict)
                    bulk_data.append({'doc': doc})
                else:
                    # # Should we insert a new record here with a generated key?
                    print("MISS", doc.get('id_nl'), "generate key?", doc)

            if bulk_data:
                done = False
                while not done:
                    try:
                        res = ES.bulk(index=ES_INDEX_NAME,
                                      body=bulk_data,
                                      refresh=True)

                        if res.get('errors') == False:
                            done = True
                            print("Committed: %i" % len(docs))
                        else:
                            errors += 1
                            print("ERROR1", errors, res)
                            time.sleep(1)
                    except:
                        errors += 1
                        e = sys.exc_info()[0]
                        print("ERROR2", errors, e)
                        time.sleep(1)
            else:
                time.sleep(1)

            bulk_data = []
            docs = []
        return
