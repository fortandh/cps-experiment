#!/usr/bin/env bash
for ((i = 1; i <= $1; i ++))
do
    python var_layout.py
    python var_scale.py
    python var_state.py
done
