#!/bin/bash

SOUNDFONT="/usr/share/sounds/sf2/FluidR3_GM.sf2"

TARGET_DIR=${1:-"./generated2"}

shopt -s nullglob

midi_files=("$TARGET_DIR"/*.mid)
if [ ${#midi_files[@]} -eq 0 ]; then
    echo "No MIDI files found in $TARGET_DIR"
    exit 1
fi

for midi_file in "${midi_files[@]}"; do
    base_name=$(basename "$midi_file" .mid)
    wav_file="${TARGET_DIR}/${base_name}.wav"
    fluidsynth -ni "$SOUNDFONT" "$midi_file" -F "$wav_file" -r 44100
    echo "Converted: $midi_file → $wav_file"
done