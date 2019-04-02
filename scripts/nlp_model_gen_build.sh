#!/bin/bash

# Important: run from root dir
rm -rf build/*
rm -rf nlp_model_gen.egg-info/*
rm -rf dist/*

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*