#!/bin/bash

if [ "z${1}" == "ztest" ] ; then
  echo "No test"
  exit
else
  sh ./scripts/start_server.sh
fi

