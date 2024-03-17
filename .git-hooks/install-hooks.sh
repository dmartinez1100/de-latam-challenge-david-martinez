#!/bin/bash
cd $(dirname $0)
ln -s -f -v $PWD/pre-push.sh ../.git/hooks/pre-push
