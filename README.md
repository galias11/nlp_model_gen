
# NLP Model creation & training API

This project is being developed under supervision of Universidad Nacional de Mar del Plata and Infolab Mar del Plata.

### Objetive
This project will offer an API for creating, training and using spaCy NLP models. It will allow to create models by theme and to use them to analyze plain text data. Administrators will be able to configure different tools for model creation and managing.

### Limits
The project is limited to the features previously defined. Although it will have services or ways to bind it to another forensic platforms, any type of integration with these kind of systems is out of scope. 

### Current status & features
- Model creation: It allows to create custom models with different search topics for both nouns and verbs. 
- Tokenizer personalization: It allows to add specific rules to tokenizer during model creation. This includes creating fuzzy tokens from original ones to get broader range of detection capacity
- Text analysis with custom models: It allows to use custom models to analyze text. Actually it gets two kind of results: The ones obtained from tokenizer and the ones obtained from entity recognition. Actually entity recognition module can not be trained.
- Model save, edit and deletion: It allows to fully manage custom models by allowing its modification or deletion.
- Word processing utilities set up (WIP): It allows to set different setups for the word processing module. This allows to manage how words are added to the tokenizer rules of the current module. This feature is implement, but integration with main controller is pending.
- Training manager module: This module allows to store, view, edit or discard examples submitted. This grants administrators a full control of model training and, at the same time, it will allow a collaborative enhancement of models. 
- Training models: This feature allows administrator to apply approved sets of training data over the models.

### Requirements
- Python 3. (Developed with python 3.7).
- MongoDB server installed on target computer.
- All python modules will be installed during package setup.

### Installation
- Run: `pip3 install nlp-model-gen`
- After package is installed run:    
MacOs: `nlp_model_gen_install.sh`    
Ubuntu: `/home/<user>/.local/bin/nlp_model_gen_install.sh`    
Windows: `python <python_path>\scripts\nlp_model_gen_install.sh`    
- For importing the model admin from ipython or python console: `from nlp_model_gen import NLPModelAdmin`
- Instanciate a new admin: `admin = NLPModelAdmin()`

### License
MIT License

Copyright (c) 2018 The Python Packaging Authority

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

This is a university project. It's usage is thought for profesionals, no further help or usage guides will be provided.
