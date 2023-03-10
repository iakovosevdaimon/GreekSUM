#!/bin/bash
cd "$(dirname "$0")"
python ./process_summarization.py
python ./compute_overlap.py
python ./split_summarization_data.py
python ./create_dataset.py
