#!/bin/bash

#Build zip packet
BUILD_DIR=/tmp/build_plugin
PLUGIN_NAME=compulink_tools

#Create if need
mkdir $BUILD_DIR

#Clear build dir
rm -R $BUILD_DIR/$PLUGIN_NAME
rm $BUILD_DIR/$PLUGIN_NAME*.zip

#Create plugin dir
mkdir $BUILD_DIR/$PLUGIN_NAME
#Copy sources
cp -R ./src/* $BUILD_DIR/$PLUGIN_NAME

#Clean
rm $BUILD_DIR/$PLUGIN_NAME/*.pyc

#Get version
cd $BUILD_DIR
VER=`grep "version=" ./$PLUGIN_NAME/metadata.txt | sed 's/version=//'`

#Zip dir
zip -9 -r $PLUGIN_NAME"_"$VER.zip ./$PLUGIN_NAME

echo "Pack for upload: $BUILD_DIR/$PLUGIN_NAME"_"$VER.zip"