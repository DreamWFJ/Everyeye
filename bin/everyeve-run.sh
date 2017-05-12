#!/bin/bash
set -e
set -o pipefail

SCRIPTNAME=$(basename $0)
LOGFILE=$NAME.log
PIDFILE=.$NAME.pid


function start(){
    if [ -f "$PIDFILE" ]; then
        echo $PIDFILE
        exit 2
    fi

    for (( ; ; ))
    do
        output "----------------------- BEGIN RUN -----------------------"
        output ""
        output "Target: $(basename $target_dir)"
        output ""
        output_printf "%-40s %9s\n" Script Seconds
        output_printf "%-40s %9s\n" --------------------------------------- ----------
        output ""

        `gunicorn --worker-class eventlet -w 1 module:app`
        sleep 5

        output ""
        output "--------------------- END RUN ---------------------"

    done &
    echo $! > $PIDFILE
}
function stop(){
    [ -f $PIDFILE ] && kill `cat $PIDFILE` && rm -rf $PIDFILE
}

function install(){
    for (( ; ; ))
    do
        output "----------------------- BEGIN INSTALL -----------------------"
        output ""
        output "Target: $(basename $target_dir)"
        output ""
        output_printf "%-40s %9s\n" Script Seconds
        output_printf "%-40s %9s\n" --------------------------------------- ----------
        output ""

        bash install.sh

        output ""
        output "--------------------- END INSTALL ---------------------"

    done &
}


case "$1" in
  start)
    start
    ;;
  stop)
    stop
    ;;
  install)
    install
    ;;
  restart)
    stop
    start
    ;;
  *)
    echo $"Usage: $0 {install|start|stop|status|restart}"
    exit 2
esac

exit $?
