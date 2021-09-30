# cmpe-273

## set up

step 1: please move to root directory of assignment as root directory with child folder as configs, src, log etc.

step 2: to ensure all dependencies are there, please execute : python3 -m pip install -r requirements.txt

step 3: please ensure test_slot is available for replication for postgres as internally the client would execute this command:
        pg_recvlogical -d college --slot test_slot --create-slot -P wal2json

step 4: plese update the mongo connection string in configs/mysql_to_mongo.json at "MONGO_CONNECTION_STRING" tag and ensure     mongo server is running 

step 5: run the client with : python3 ./src/client.py

step 6: run the server with : python3 src/init_server.py 

step 7: please execute pg_recvlogical -d postgres --slot test_slot --drop-slot to ensure that slot is free for use.