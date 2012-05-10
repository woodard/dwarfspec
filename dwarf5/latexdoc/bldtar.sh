#!/bin/bash
suf=""
if [ $# -eq 0 ]
then
  suf=""
else
  if [ $# -eq 1 ]
  then
    suf=$1
  else 
    echo "Oops, too many args, exit"
    exit 1
  fi
fi
echo proceed with $suf.
targ=/var/tmp
n=DW5$suf
rm  -rf $targ/$n $targ/$n.tar        
mkdir $targ/$n
cp * $targ/$n
cd $targ
tar cf $n.tar $n
ls -l $n.tar $n
        

