#!/bin/sh
export DISPLAY=":1"

NAME=`xdotool getactivewindow getwindowname`
# Append suffix to clarify hidden application names.
CMD=`ps -o cmd= fp \`xdotool getactivewindow getwindowpid\``
# Nautilus.
NAME="$NAME`echo $CMD | sed -nr 's/.*(nautilus).*/ - \1/p'`"
# JetBrains.
NAME="$NAME`echo $CMD | sed -nr 's/.*-Didea.platform.prefix=([a-zA-Z]*) .*/ - \1/p'`"

IDLE=`xprintidle`

echo `date "+%H:%M"`,$IDLE,$NAME >> /home/sichaoyang/Diary/logs/raw/`date "+%Y%m%d"`.csv
