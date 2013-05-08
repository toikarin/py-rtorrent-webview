#!/usr/bin/env bash

script_dir=$(dirname $(readlink -f "$0"))
project_dir=$(dirname "${script_dir}")

type -P virtualenv &> /dev/null || {
   echo "virtualenv not installed."
   exit 1
}

virtualenv --no-site-packages --distribute "${project_dir}/virtualenv"
source "${project_dir}/virtualenv/bin/activate"
pip install -r "${project_dir}/requirements.txt"
