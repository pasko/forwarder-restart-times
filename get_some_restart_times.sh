#!/bin/bash

for build in 22162 22161 22160 22159 22158 22157 22156 22155 22154 22153; do
  wget 'http://build.chromium.org/p/chromium.linux/builders/Android%20Tests%20%28dbg%29/builds/'$build'/steps/slave_steps/logs/stdio/text' -O android_tests_dbg_$build.log
done

for build in 22162 22161 22160 22159 22158 22157 22156 22155 22154 22153; do
  echo Build $build: $(python process_log.py <android_tests_dbg_$build.log)
done
