#!/usr/bin/env bash
for ((i = 1; i <= $1; i ++))
do
    python ./case_generator/var_layout.py
    python ./case_generator/var_scale.py
    python ./case_generator/var_state.py
done