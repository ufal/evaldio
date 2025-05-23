#!/bin/bash

xmllint --format - |
    grep "<u " |
    sed 's|^.*who="\([^"]*\)".*>\(.*\)</u>$|\1: \2|'