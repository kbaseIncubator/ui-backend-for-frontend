#!/bin/bash

if [ "z${1}" == "ztest" ] ; then
  echo "No test"
  exit
elif [ "z${1}" == "zreport" ] ; then
  echo "Report"
  [ -e work ] || mkdir work
  echo "{'bogus':'report'}" > /kb/module/work/compile_report.json
elif [ "z${1}" == "zbash" ] ; then
  bash
else
  sh ./scripts/start_server.sh
fi

