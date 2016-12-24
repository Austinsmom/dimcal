#!/bin/bash -x
OLDDIR=`pwd`

dropdb --if-exists dimcaldb
createdb --owner=dimcaluser dimcaldb

# Migrations use relative paths so it's important to run them from project root
cd ${TRAVIS_BUILD_DIR}/src/dimcal/
./manage.py migrate
uwsgi --master                                     \
      --socket 127.0.0.1:3031                      \
      --module=dimcal.wsgi:application             \
      --env DJANGO_SETTINGS_MODULE=dimcal.settings \
      --http :8000                                 \
      --processes 8 --threads 2                    \
      --stats 127.0.0.1:9191                       &
echo "Waiting 11sec for the server to start"
sleep 11s
echo "Starting crawl"
cd ${TRAVIS_BUILD_DIR}/wget_build/

# Thanks: http://stackoverflow.com/a/11850469/266387
./extract_links.py | xargs -n 1 -P 8 \
                 wget --recursive --no-host-directories --quiet

rm dim_calendar/about # This is configured on s3 with a redirect
cd ${OLDDIR}
echo **************************************** DONE! ****************************************

