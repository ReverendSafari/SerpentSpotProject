#!/bin/bash

for file in *.jpg; do
    mv "$file" "$(echo $file | tr 'A-Z' 'a-z')"
done
