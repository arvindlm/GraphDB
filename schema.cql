CREATE KEYSPACE IF NOT EXISTS sample
WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 3};

USE sample;

DROP TABLE IF EXISTS node;
CREATE TABLE node(
   id uuid PRIMARY KEY
);

DROP TABLE IF EXISTS edge;
CREATE TABLE edge(
   node_id uuid,
   id uuid,
   destination uuid,
   PRIMARY KEY (node_id, id)
);