#!/bin/bash

# define path to custom docker environment
DOCKER_ENVVARS=/etc/apache2/docker_envvars

# write variables to DOCKER_ENVVARS
cat << EOF > "$DOCKER_ENVVARS"
export APACHE_RUN_USER=www-data
export APACHE_RUN_GROUP=www-data
export APACHE_LOG_DIR=/var/log/apache2
export APACHE_LOCK_DIR=/var/lock/apache2
export APACHE_PID_FILE=/var/run/apache2.pid
export APACHE_RUN_DIR=/var/run/apache2
EOF

# source environment variables to get APACHE_PID_FILE
. "$DOCKER_ENVVARS"

# only delete pidfile if APACHE_PID_FILE is defined
if [ -n "$APACHE_PID_FILE" ]; then
   rm -f "$APACHE_PID_FILE"
fi

# start other services


# line copied from /etc/init.d/apache2
ENV="env -i LANG=C PATH=/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"




LAUNCHER_TEMPLATE_PATH=/data/pvw/conf/launcher_template.json
LAUNCHER_PATH=/data/pvw/conf/launcher.json
ROOT_URL="ws://localhost"

if [ ! -z "${SERVER_NAME}" ]
then
  ROOT_URL="ws://${SERVER_NAME}"
fi



INPUT=$(<"${LAUNCHER_TEMPLATE_PATH}")
echo $INPUT
echo $ROOT_URL

OUTPUT="${INPUT//"SESSION_URL_ROOT"/$ROOT_URL}"
echo -e "$OUTPUT" > "${LAUNCHER_PATH}"



export DISPLAY=:0.0
export PYTHONPATH="/data/pv/pv-5.9/lib64/python3.8/site-packages/"
export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:/data/pv/pv-5.9/lib64
export PATH=$PATH:/data/pv/pv-5.9/bin

#cat ${LAUNCHER_PATH}
#/bin/bash
echo "Starting the wslink launcher"
python /data/pv/pv-5.9/lib64/python3.8/site-packages/wslink/launcher.py ${LAUNCHER_PATH}  &
#vtkpython /data/pv/pv-5.9/share/vtkjsserver/vtkw-server.py --port 1234 --host 0.0.0.0
echo "Starting the wslink launcher"

# use apache2ctl instead of /usr/sbin/apache2
$ENV APACHE_ENVVARS="$DOCKER_ENVVARS" apache2ctl -D FOREGROUND
#service apache2 reload
/usr/sbin/apache2ctl -D FOREGROUND

# service apache2 restart 
