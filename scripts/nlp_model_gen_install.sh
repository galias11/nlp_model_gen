#!/usr/bin/env python

import os
import subprocess

os_name = os.name
base_model_install_script = 'python -m spacy download es_core_news_md' if os.name == 'nt' else 'python3 -m spacy download es_core_news_md'

subprocess.run(base_model_install_script.split())