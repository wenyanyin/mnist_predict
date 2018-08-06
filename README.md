# mnist_predict
use trained mnist model to predict number from user input image through Flask service and store image data in database

## Overview
1. Creating the tranied MNIST model.
2. Building the docker image.
3. Runing the cassandra service.
4. Running the built project docker container.
5. Openning your browser, and go to page **http://localhost:4000/uploads**
6. Uploading your own handwriting image (*xxx.png*), the recognised data will be displayed and the data will be stored in the database.
7. Connecting to cassandra from **cqlsh**
8. Checking your message stored. 
### Done!
--------------------------------------------------------------------------------------------------------------------------

## Package Dependencies
- *Docker* (The whole project will be running in the docker container)
- *Cassandra* (NoSQL type database)

## MNIST MODEL 
There is already exists an tranied mnist model which has been trained 70,000 times (Path: *mnist_predict/mnist_model/trained_model*)

The train-data-set is already in the directory
### Continuing training model
If you are not satisfied with the accuracy of the model, you can always continue to train it.
- FILE: mnist_predict/mnist_model/**mnist_deep_continue.py**

`python mnist_deep_continue.py`

### Initialising model
If you want to start your own train loop or creat new model, please use following"
- FILE: mnist_predict/mnist_model/**mnist_deep_creat.py**

`python mnist_deep_creat.py`

#### Creating an image file
You have to create a PNG file that contains a handwritten number. The background has to be white and the number has to be black. Any paint program should be able to do this. Also the image has to be auto cropped so that there is no border around the number.

### Try directly predict number
The easiest way again is to put the image file in the same directory as the python scripts and cd to the directory where the python files are located. (Path: mnist_predict/**predict_deep.py**)

The predict scripts require one argument: the file location of the image file containing the handwritten number. For example when the image file is ‘xxx.png’ and is in the same location as the script, run:

`python predict_deep.py xxx.png`

It is convieniet to run **predict_deep.py** directly to check the precision of the *mnist_model*, and add any change before build docker image.

--------------------------------------------------------------------------------------------------------------------------

## Running in the docker container

### Building the docker image
**cd** to the project directory *mnist_predict*, using -t to provide a friendly name

``` docker build -t mnist_predict . ```

run `docker image ls` see if it has been created.

> ### Troubleshooting
>- Never forget there is a `.` behind image name, otherwise it will report bug.
>- Notice that inside **Dockerfile**, the resource of `pip install` was using *pypi.tuna.tsinghua.edu.cn/simple*, because of the Chinese Internet protocols (GFW). Instead, if you are out of mainland China, you can feel free to change it to the original source *pypi.python.org* in case it is too slow or readtime out and failed.

### Starting a cassandra server instance
``` docker run --name project-cassandra -p 9042:9042 -d cassandra:latest ```

- -p port expose and connect, -d run process in background

### Running the container
```docker run --name test -p 4000:80 --rm -d mnist_predict```
- container name: test, image used: mnist_predict, port:4000->80, --rm remove the old version after finishing process

> ### Troubleshooting 
> #### Cannot connect to Cassandra
>- First of all, run `docker ps` see if cassandra has been running *project-cassandra*
>>- If Yes, then run `python database_connect.py xxx.png xxx` (two arguments required) see if it is working. 
>>> 	If NO, change *data_connect.py* line 19, the value of contact_points ('172.17.0.2') to your local machine IP, find your local host by command `docker-machine ip` then run `python database_connect.py xxx.png xxx` again










