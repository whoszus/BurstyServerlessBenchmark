export CLASSPATH=gson-2.8.2.jar
javac Md5.java
jar cvf Md5.jar Md5.class
wsk -i action create md5-java Md5.jar --main Md5
wsk -i action invoke md5-java --result