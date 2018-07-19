#
#  The purpose of this Dockerfile is to test out my dotfiles repository
#
#	rebuild image: docker build -t dotfiles-tester:latest --build-arg CACHE_DATE=$(date +%Y-%m-%d:%H:%M:%S) .
#	run container: docker run -it dotfiles-tester /bin/bash

FROM ubuntu:latest

MAINTAINER Doug Morand <dmorand@gmail.com>

RUN apt-get update -y && apt-get install -y \
	curl \
	git \
	vim \
	sudo

# add dotfiles user
RUN adduser dotfiles --disabled-password --gecos ""                      && \
    echo "ALL            ALL = (ALL) NOPASSWD: ALL" >> /etc/sudoers && \
    chown -R dotfiles:dotfiles /home/dotfiles                                 

# dotfiles user config
USER dotfiles
ENV HOME /home/dotfiles

# Hack used to ensure that the git clone isn't cached
ARG CACHE_DATE=2016-01-01

# get dotfiles
RUN cd $HOME && \ 
    git clone https://github.com/dmorand17/dotfiles.git
