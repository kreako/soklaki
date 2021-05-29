#!/usr/bin/bash

set -e

DT=$(date +"%Y_%m_%d_%H_%M_%S")

cd $HOME/backup/

cp $HOME/backup.sh .

# Postgresql dump
cd pg_dump/

podman exec -it soklaki-db pg_dump -d postgres -h 127.0.0.1 -U postgres > dump_${DT}.sql
gzip dump_${DT}.sql

cd ../..

# Reports copy
rsync -azr $HOME/reports/ $HOME/backup/reports/

# Remote copy
rsync -azr $HOME/backup/ backup:backup/
rsync -azr $HOME/backup/ prom:backup/
