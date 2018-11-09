#!/usr/bin/env bash

isort -rc .
yapf -r . --in-place