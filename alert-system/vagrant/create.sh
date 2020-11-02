#!/usr/bin/env bash

if [ ! "$(command -v vagrant)" ]; then
  echo "Please, install vagrant first"
  exit 1
elif [ ! "$(command -v virtualbox)" ]; then
  echo "Please, install virtualbox first"
  exit 1
fi

vagrant box add --provider virtualbox ubuntu/bionic64 2> /dev/null
vagrant box update
vagrant up