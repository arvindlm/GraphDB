CREATE KEYSPACE IF NOT EXISTS zeus
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 2};

USE zeus;

DROP TABLE IF EXISTS node;
CREATE TABLE node(
   zid uuid PRIMARY KEY
);

DROP TABLE IF EXISTS edge;
CREATE TABLE edge(
   node_id uuid,
   zid uuid,
   destination uuid,
   PRIMARY KEY (node_id, zid)
);
