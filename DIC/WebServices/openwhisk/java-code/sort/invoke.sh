export CLASSPATH=gson-2.8.2.jar
javac Sort.java
jar cvf Sort.jar Sort.class
wsk -i action create sort-java Sort.jar --main Sort
wsk -i action invoke sort-java --result