import apis.zeusdb
import index
from time import time


def get_weight_from_db():
	query = "select * from node where weight <= 10 allow filtering"
	rows = zeusdb.session.execute(query);
	count = 0
	for row in rows:
		count += 1
	return count

query_body = {
       "query" : {
            "range" : {
                "weight" : {
                    "lte": 10
                }
            }
	}

}

start_time = time()
res = index.search_all_indexes(zeusdb.NODE_TABLE ,query_body)
for r in res:
	print r
	index.delete_record_from_index(r)
	a = zeusdb.get_node_by_id(str(r))
 	print "here"
	print a
end_time = time()
print "With Indexing"
print "Length of results returned: " + str(len(res))
print "Time taken for query: " +  str(end_time - start_time)

start_time = time()
res = get_weight_from_db()
end_time = time()
print "\n\nWithout Indexing"
print "Length of results returned: " + str(res)
print "Time taken for query: " + str(end_time - start_time)
