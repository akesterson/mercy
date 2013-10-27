#!/bin/bash

cat <<EOF
name 'akesterson-mercy'
version '${MAJOR}-${BUILD}'
dependency 'apache/apache'
summary 'Puppet module for deploying the mercy web application'
description 'Puppet module for deploying the mercy web application'
project_page http://github.com/akesterson/mercy/tree/master/puppet
license 'MIT'
author 'Andrew Kesterson <andrew@aklabs.net>'
EOF
