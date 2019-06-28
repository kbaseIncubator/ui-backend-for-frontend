#!/bin/bash

if [ "z${1}" == "ztest" ] ; then
  echo "No test"
  exit
elif [ "z${1}" == "zreport" ] ; then
  echo "Report"
  [ -e work ] || mkdir work
  echo "{}" > ./work/compile_report.json
  exit
else
  sh ./scripts/start_server.sh
fi

