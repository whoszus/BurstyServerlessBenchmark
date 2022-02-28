export CLASSPATH=gson-2.8.2.jar
javac Hello.java
jar cvf Hello.jar Hello.class
wsk -i action create hello-java Hello.jar --main Hello
wsk -i action invoke hello-java --result