#!/usr/bin/env bash

on_die() {
   kill $(jobs -p)
}

trap 'on_die' EXIT

script_dir=$(dirname $(readlink -f "$0"))
project_dir=$(dirname "${script_dir}")

source "${project_dir}/virtualenv/bin/activate"
python "${project_dir}/server.py"
