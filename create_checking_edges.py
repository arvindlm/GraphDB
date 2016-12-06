import zeus
import json
import time

INPUT_FILE = 'checkin_edges.txt'
total = sum(1 for line in open(INPUT_FILE))
print 'Total edges =',total
start_time = time()
with open(INPUT_FILE) as infile:
    for line in infile:
    	print type(line)
    	edge = eval(unicode(line))
		zeusdb.create_edge(edge)
		sys.stdout.write("\rCreated "+str(i)+" edges out of "+str(total)+" edges")
		sys.stdout.flush()
end_time = time()
print
print "It took " + str(end_time-start_time) + " seconds to create " + str(total) + " edges"
