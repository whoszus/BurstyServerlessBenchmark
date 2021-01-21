export CLASSPATH=gson-2.8.2.jar
javac Hash.java
jar cvf Hash.jar Hash.class
wsk -i action create hash-java Hash.jar --main Hash
wsk -i action invoke hash-java --result