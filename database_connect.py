import logging
import os,sys
import time
import datetime

log = logging.getLogger()
log.setLevel('INFO')
handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter("%(asctime)s [%(levelname)s] %(name)s: %(message)s"))
log.addHandler(handler)

#from cassandra import ConsistencyLevel
from cassandra.cluster import Cluster
from cassandra.query import SimpleStatement


#ip=os.popen(docker inspect -f '{{ .NetworkSettings.IPAddress }}' project-cassandra)
#ip_address=ip.read()
cluster = Cluster(contact_points=['172.17.0.2'],port=9042)
session = cluster.connect()


KEYSPACE = "mnistpredict"

def createKeySpace():
    log.info("Creating keyspace...")
    try:
        session.execute("""
            CREATE KEYSPACE IF NOT EXISTS %s
            WITH replication = { 'class': 'SimpleStrategy', 'replication_factor': '2' }
            """ % KEYSPACE)

        log.info("setting keyspace...")
        session.set_keyspace(KEYSPACE)

        log.info("creating table...")
        session.execute("""
            CREATE TABLE IF NOT EXISTS mnistable (
                record_time text,
                image_name text,
                predict_number text,
                PRIMARY KEY (record_time, image_name)
            )
            """)
    
    except Exception as e:
        log.error("Unable to create keyspace")
        log.error(e)


def insertdata(argv):
    log.info("Inserting uploaded image information...")
    current_time=datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    try:
        session.execute(
            "INSERT INTO mnistable (record_time, image_name, predict_number) VALUES (%s, %s, %s)", [current_time, argv[1], argv[2]]
            #{'record_time':current_time, 'image_name':argv[1], 'predict_number':argv[2], }
            )
    except Exception as e:
        log.error("Unable to insert data")
        log.error(e)

def main(argv):
    """
    Main function.
    """
    createKeySpace();
    insertdata(argv);
    
if __name__ == "__main__":
    main(sys.argv)