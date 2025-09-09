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

folder with dal dbs - mongodb, elastic  (used in step-2 and step-3)  

- class **DALElastic** for connection and operations be elasticsearch  
- class **DALMongo** for connection and operations be mongodb   


### kafka_tools  

folder with tools for kafka communication  (used in step-1 and step-2)   

- class **Producer** for produce messages to kafka
- class **Consumer** for consume messages from kafka  


### step 3 - STT  

folder with STT tolls. and transcription process -  

transcription process pulls out the files-id from elastic,  
loads all file by his id from mongodb, transcriber him,  
and save the text back in elastic.

i chose to build the transcript as a separate process.  
because it is a separate process from uploading the file itself and their metadata,
and it will probably take a long time.  

- file **speach_to_text** with method to convert STT  
- file **transcription_manager** with **Transcriber** class for for management the process  
