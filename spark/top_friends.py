from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkConf

conf = SparkConf() \
    .setAppName("ZeusDB") \
    .setMaster("local") \
    .set("spark.cassandra.connection.host", "YOUR_CLUSTER_HOST_NAME")

sc = CassandraSparkContext(conf=conf)

result = sc.cassandraTable("zeus", "edge") \
    .select("destination", "type") \
    .filter(lambda x: x["type"] == "friend") \
    .map(lambda x: (x["destination"], 1)) \
    .reduceByKey(lambda a, b: a + b) \
    .top(10, key=lambda x: x[1])

print
print "================================"
print "TOP 10 PEOPLE WITH MOST FRIENDS"
print "================================"
for row in result:
    print str(row[0]) + "\t\t" + str(row[1])
print
print "================================"
print
