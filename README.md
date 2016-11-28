# Zeus DB
### A simple graph database built using Cassandra


## Commands
-To run schema,
```
cqlsh -f schema.cql
```

## Installing python driver
```
apt-get install python-pip
apt-get install gcc python-dev
apt-get install libev4 libev-dev
pip install --install-option="--no-cython" cassandra-driver
```

# Installing cassandra
First install java
```
sudo add-apt-repository ppa:webupd8team/java
sudo apt-get update
sudo apt-get install oracle-java8-installer
```
Then, install Cassandra
```
echo deb http://debian.datastax.com/community stable main | sudo tee -a /etc/apt/sources.list.d/cassandra.sources.list
curl -L http://debian.datastax.com/debian/repo_key | sudo apt-key add -
sudo apt-get update
sudo apt-get install cassandra=3.0.0
sudo service cassandra status
```
Now, open config at /etc/cassandra/cassandra.yaml and
	- set listen_address to the private ip
	- set broadcast_address to the public ip
	- set rpc_address to 0.0.0.0
	- set broadcast_rpc_address to the private ip
	- set seeds in seed_provider to a comma separated list of all the public ip in the cluster
Finally, restart cassandra
```
service cassandra restart
```

In case of confusions, just go to [this link](broadcast_rpc_address) and follow method 2