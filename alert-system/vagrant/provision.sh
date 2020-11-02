#!/usr/bin/env bash

mkdir /system_init && cd /system_init || exit
apt-get update
apt-get install -y g++ clang git wget tar make cmake gdb gdbserver
# installing openssl
apt-get install -y openssl
openssl version

# installing boost
apt-get install -y libboost-system-dev libboost-thread-dev libboost-log-dev \
    libboost-program-options-dev libboost-chrono-dev libboost-locale-dev libboost-random-dev
# installing cpprestsdk and dependecies
apt-get install -y libcpprest-dev
# installing dependencies for grcp and downloading repo
apt-get install -y build-essential
git clone https://github.com/grpc/grpc.git

protobuf_version=3.11.4

# installing protobuf (for etcd client) and dependencies
apt-get install -y autoconf automake libtool curl unzip
wget https://github.com/protocolbuffers/protobuf/releases/download/v$protobuf_version/protobuf-cpp-$protobuf_version.tar.gz
tar -xzvf protobuf-cpp-$protobuf_version.tar.gz
cd /system_init/protobuf-$protobuf_version/ || exit
./configure
make
# make check
make install
ldconfig

# installing grpc (for etcd client) and dependencies
cd /system_init/grpc/ || exit
git submodule update --init
make
make install

# installing clang-tidy and dependencies
apt-get install -y clang-tidy python3-pip

cd / && rm -rf /system_init