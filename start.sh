#!/usr/bin/env bash

python -m spacy download en_core_web_sm

streamlit run dashboard.py --server.port $PORT --server.address 0.0.0.0