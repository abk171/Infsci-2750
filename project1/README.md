## Miniproject 1

### Part 1: Setting up Docker
1. Download the Docker file. Create xml files (hdfs-site.xml, core-site.xml) according to the following [link](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html) for pseudo-distributed operation.

`etc/hadoop/hdfs-site.xml`
```xml
<configuration>
    <property>
        <name>dfs.replication</name>
        <value>1</value>
    </property>
</configuration>
```

`etc/hadoop/core-site.xml`
```xml
<configuration>
    <property>
        <name>fs.defaultFS</name>
        <value>hdfs://localhost:9000</value>
    </property>
</configuration>
```


2. Build the Docker container and open a shell.

3. edit xml files such that vm-1 is set to localhost. 

4. edit /opt/hadoop/sbin/start-dfs.sh -> put startdfs.txt at the start of the file (available on canvas under modules)
```bash
HDFS_DATANODE_USER=root
HADOOP_SECURE_DN_USER=hdfs
HDFS_NAMENODE_USER=root
HDFS_SECONDARYNAMENODE_USER=root
```

5. edit /opt/hadoop/sbin/start-yarn.sh -> put startyarn.txt at the start of the file (available on canvas under modules)
```bash
YARN_RESOURCEMANAGER_USER=root
HADOOP_SECURE_DN_USER=yarn
YARN_NODEMANAGER_USER=root
```
6. go to this [link](https://hadoop.apache.org/docs/stable/hadoop-project-dist/hadoop-common/SingleCluster.html) and check commands to generate ssh keys (setup passphraseless ssh (pseudo distributed)) 

```shell
ssh-keygen -t rsa -P '' -f ~/.ssh/id_rsa
cat ~/.ssh/id_rsa.pub >> ~/.ssh/authorized_keys
chmod 0600 ~/.ssh/authorized_keys
```

7. restart ssh daemon `/etc/init.d/ssh start`
8. `/opt/hadoop/bin/hadoop namenode -format`
9. `/opt/hadoop/sbin/start-dfs.sh`
10. `/opt/hadoop/sbin/start-yarn.sh`

The `jps` command should give the following output:
```shell
root@36fe57539718:/# jps
1156 NodeManager
1004 ResourceManager
1533 Jps
334 NameNode
718 SecondaryNameNode
```

### Part 2: ngram calculator
The program calculates the ngram, which is a contiguous sequence of n characters from a given sequence of text. 

#### Compilation:
```shell
javac -classpath $(/opt/hadoop/bin/hadoop classpath) -d . .
jar -cvf ngram.jar -C . *.class
```

#### Creating directories:
```shell
/opt/hadoop/bin/hdfs dfs -mkdir /input
/opt/hadoop/bin/hdfs dfs -put /opt/hadoop/etc/hadoop/*.xml /input 
```

#### Execution
```shell
/opt/hadoop/bin/hadoop jar ngram.jar ngram /input /output 3
```

### Part 3: Access log
The following porgrams run searching commands on a large `access_log` file.


