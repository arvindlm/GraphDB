from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkConf

conf = SparkConf() \
    .setAppName("ZeusDB") \
    .setMaster("local") \
    .set("spark.cassandra.connection.host", "YOUR_CLUSTER_HOST_NAME")

sc = CassandraSparkContext(conf=conf)

result = sc.cassandraTable("zeus", "edge") \
    .select("destination", "visit_count", "type") \
    .filter(lambda x: x["type"] == "visited") \
    .map(lambda x: (x["destination"], int(x["visit_count"]))) \
    .reduceByKey(lambda a, b: a + b) \
    .top(10, key=lambda x: x[1]) \

print
print "================================"
print "TOP 10 FREQUENTLY VISITED PLACES"
print "================================"
for row in result:
    print str(row[0]) + "\t\t" + str(row[1])
print
print "================================"
print
