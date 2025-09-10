# the muezzin project

---

### step 1 - retrieval

service which is responsible for retrieving metadat of files
and send all one to kafka.  

- class **FileMetadata**  for easy access metadata-file  
- class **Manager** for manage the process  

---

### step 2 - db_uploader  

service which is responsible for upload files and their metadata to dbs (mongodb and elastic)
from kafka (uses be kafka consumer)  

- class **UploadManager** for run all process   
uses be kafka-consumer to get the metadata of files  
creates unique id for all file by his metadata and  store it as follows:  
uses be DAL-elastic and sending to him the metadata  
uses be DAL-mongodb and sending to him the files themselves


### DAL  

folder with dal dbs - mongodb, elastic  (used in step-2, step-3, step4)  

- class **DALElastic** for connection and operations be elasticsearch  
- class **DALMongo** for connection and operations be mongodb   


### kafka_tools  

folder with tools for kafka communication  (used in step-1 and step-2)   

- class **Producer** for produce messages to kafka
- class **Consumer** for consume messages from kafka  

---

### step 3 - STT  

folder with:  

- STT tolls.  
- service of transcription process -  

    transcription process pulls out the files-id from elastic,  
    loads all file by his id from mongodb, transcriber him,  
    and save the text back in elastic.

    i chose to build the transcript as a separate process.  
    because it is a separate process from uploading the file itself and their metadata,
    and it will probably take a long time.  


- file **speach_to_text** with method to convert STT  
- file **transcription_manager** with **Transcriber** class for for management the process  

---

### step 4 - classification  

service which is responsible for classified risk level of texts which is stored in elastic-index.  
retrieves all documents from elastic, classified them one by one - by words from hostile lists,  
and update her risk level back to elastic-index.  

- file **text_analysis** with auxiliary functions which locate how many times a word or sentence appears in the text.  
- class **Classified** responsible for risk calculation method. accepts only two numeric data - 1: length text, 2: num hostile words which were found in the text.  
  calculate three things:  
  - **risk percent** - the formula: num of hostile_words divide by tenth the length of the text, ranges from zero to one max  
  - **threshold determination** - the formula: risk_percent greater than 0.1.  
  - **danger level** - the formula: "high" if risk_percent greater than 0.75, "medium" if risk_percent greater than 0.1, less "none" .  

- class **ClassifiedManager** to manage the process, retrieves, classified, updates the elastic.  
- file **main** stores the hostile lists deciphering them and init the ClassifiedManager  


- **notes** : 
  - ClassifiedManager receives dict of lists hostile_words with kwy of level their risk and the final risk calculation will be divided by the level of risk.  
  This way he can get many lists at many risk levels.   
  adaptation to the specific requirement of the project i called him  in the main with  {1: hostile_words , 2: lass_hostile_words}.  
  - i chose to perform the risk calculations based on the percentage of dangerous words in the text, regardless of other texts.  
  it is possible to change all calculations functions in classified class only, and all the code will run as is.  

---

### step 5 - docker  

- i added to all the four services **requirements.txt** that contain their needs and **Dockerfile** customized  
- in addition there is a file **docker_commends.bat** that contain all the required Docker commands 
for all the services and mongodb, elastic, kafka - which are consumed for running. all under one network.

---

### environment variables  

the project has many environment variables. most of them are in the **configs** folder.  
initialized with default values ​​for local execution when mongodb, elastic, and kafka running in the background and listening to the usual ports.  

- mongodb env:  
MONGO_PREFIX  (default - 'mongodb')  
MONGO_HOST  (default 'localhost')  
MONGO_USER  (default None - not necessarily necessary)   
MONGO_PASSWORD  (default None - not necessarily necessary)   
MONGO_DB  (default 'muezzin')   
MONGO_COLLECTION  (default 'podcast') 


- elasticsearch env  
ES_HOST_NAME  (default 'localhost')   
ES_INDEX  (default 'muezzin')   
ES_MAPPINGS  (there is a default value bat the variable itself is not necessary)   


- kafka env  
KAFKA_SERVER_URI  (default 'localhost:9092')   
KAFKA_PRODUCER_TOPIC  (default 'podcast_metadata')  
KAFKA_CONSUMER_GROUP  (default 'muezzin-group')  


- logger env  
LOGGER_NAME  (default 'logger-muezzin')  
LOGGER_ES_HOST  (default 'http://localhost:9200')  
LOGGER_ES_INDEX  (default 'logging-muezzin')


- retrieval env   
SOURCE_FOLDER_PATH  (default 'C:\\python_data\\podcasts')  
The folder from which the files will be pulled and the process will be carried out on them  
for running in a docker is necessary define --mount with src={SOURCE_FOLDER_PATH} and dst=app/data      
