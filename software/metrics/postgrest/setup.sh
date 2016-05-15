#!/bin/bash

createdb openawg
createuser anonymous
sqitch deploy

