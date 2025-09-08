# the muezzin project

### step 1 - retrieval

service who is responsible for retrieving metadat of files
and send all one to kafka.  

- class **FileMetadata**  for easy access metadata-file  
- class **Manager** for manage the process  


### step 2 - db_uploader  

service who is responsible for upload files and their metadata to dbs (mongodb and elastic)
from kafka (uses be kafka consumer)  

- class **UploadManager** for run all process   
uses be kafka-consumer to get the metadata of files  
creates unique id for all file by his metadata and  store it as follows:  
uses be DAL-elastic and sending to him the metadata  
uses be DAL-mongodb and sending to him the files themselves


### DAL  

folder with dal dbs - mongodb, elastic  (used in step2)  

- class **DALElastic** for connection and operations be elasticsearch  
- class **DALMongo** for connection and operations be mongodb   


### kafka_tools  

folder with tools for kafka communication  (used in step1 and step2)   

- class **Producer** for produce messages to kafka
- class **Consumer** for consume messages from kafka  


