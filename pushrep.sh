#!/bin/bash
git --git-dir=$HOME/blue-green/.git --work-tree=$HOME/blue-green push add .
git --git-dir=$HOME/blue-green/.git --work-tree=$HOME/blue-green commit . -m "updated version"
git --git-dir=$HOME/blue-green/.git --work-tree=$HOME/blue-green push origin main
