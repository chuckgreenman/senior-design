#!/bin/bash

script_dir=$(dirname $0)
export FLASK_APP=$script_dir/flaskr
export FLASK_ENV=development
flask run