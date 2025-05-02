#!/bin/bash

SCRIPT_TEXT="$1"

aws polly synthesize-speech \
  --output-format mp3 \
  --voice-id Matthew \
  --text "$SCRIPT_TEXT" \
  speech.mp3


