# Build -----------------------------------------------------

FROM ubuntu:latest as build

# creating build directory
ADD ./ /app/alert-system
WORKDIR /app/build/

RUN apt-get update && \
    apt-get install -y \
        g++ git wget tar make cmake \
# installing openssl
        openssl && \
    openssl version && \
# installing boost
    apt-get install -y \
        libboost-system-dev \
        libboost-thread-dev \
        libboost-log-dev \
        libboost-program-options-dev \
        libboost-chrono-dev \
        libboost-locale-dev \
        libboost-random-dev \
# installing cpprestsdk and dependecies
        libcpprest-dev \
# installing dependencies for grcp and downloading repo
        build-essential && \
    git clone https://github.com/grpc/grpc.git

ARG protobuf_version=3.11.4

# installing protobuf (for etcd client) and dependencies
RUN apt-get install -y autoconf automake libtool curl unzip && \
    wget https://github.com/protocolbuffers/protobuf/releases/download/v$protobuf_version/protobuf-cpp-$protobuf_version.tar.gz && \
    tar -xzvf protobuf-cpp-$protobuf_version.tar.gz
WORKDIR /app/build/protobuf-$protobuf_version/
RUN ./configure && \
    make && \
#    make check && \
    make install && \
    ldconfig

# installing grpc (for etcd client) and dependencies
WORKDIR /app/build/grpc/
RUN git submodule update --init && \
    make && \
    make install

# building project
WORKDIR /app/build/
RUN cmake ../alert-system && \
    make test_full_delivery

# Run -----------------------------------------------------

FROM ubuntu:latest

# installing libcpprest library to run app
RUN apt-get update && \
    apt-get install -y \
        libcpprest \
        libboost-system-dev libboost-thread-dev libboost-log-dev \
        libboost-program-options-dev libboost-chrono-dev \
        libboost-locale-dev libboost-random-dev \
    && \
# setting user
    groupadd -r alert_system && useradd -r -g alert_system alert_system



USER alert_system

WORKDIR /app/
COPY --from=build /app/build/executables/test_full_delivery .

ENTRYPOINT ["./test_full_delivery"]


