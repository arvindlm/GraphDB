from pyspark_cassandra import CassandraSparkContext
from pyspark import SparkConf

conf = SparkConf() \
    .setAppName("ZeusDB") \
    .setMaster("local") \
    .set("spark.cassandra.connection.host", "YOU_CLUSTER_HOST_NAME")

sc = CassandraSparkContext(conf=conf)

def retTuple(r):
    age = int(r["age"])
    if age < 20:
        return ("<20", 1)
    if age < 40:
        return ("20 < 40", 1)
    if age < 60:
        return ("40 < 60", 1)
    return (">60", 1)

result = sc.cassandraTable("zeus", "node") \
    .select("age") \
    .where("type=?", "person") \
    .map(retTuple) \
    .reduceByKey(lambda a, b: a + b) \
    .collect()

print
print "================================"
print "AGE DEMOGRAPHICS"
print "================================"
for row in result:
    print str(row[0]) + "\t\t" + str(row[1])
print
print "================================"
print
