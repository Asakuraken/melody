import os
import numpy as np
import pretty_midi

def compute_note_density(pm):
    total_notes = sum(len(inst.notes) for inst in pm.instruments)
    duration = pm.get_end_time()
    return total_notes / duration if duration > 0 else 0

def compute_pitch_histogram(pm):
    all_pitches = [note.pitch for inst in pm.instruments for note in inst.notes]
    histogram = np.zeros(128)
    for pitch in all_pitches:
        histogram[pitch] += 1
    return histogram / np.sum(histogram) if np.sum(histogram) > 0 else histogram

def compute_ioi_stats(pm):
    ioi_list = []
    for inst in pm.instruments:
        times = sorted(note.start for note in inst.notes)
        ioi_list.extend(np.diff(times))
    ioi = np.array(ioi_list)
    return np.mean(ioi) if len(ioi) > 0 else 0, np.std(ioi) if len(ioi) > 0 else 0

def analyze_midi_file(filepath):
    try:
        pm = pretty_midi.PrettyMIDI(filepath)
        density = compute_note_density(pm)
        mean_ioi, std_ioi = compute_ioi_stats(pm)
        return density, mean_ioi, std_ioi
    except Exception as e:
        return None, None, None

def analyze_directory(directory):
    note_density_list = []
    IOI_average_list = []
    IOI_std_list = []
    for filename in os.listdir(directory):
        if filename.endswith('.mid') or filename.endswith('.midi'):
            note_density, mean_ioi, std_ioi = analyze_midi_file(os.path.join(directory, filename))
            if note_density is not None:
                note_density_list.append(note_density)
                IOI_average_list.append(mean_ioi)
                IOI_std_list.append(std_ioi)
    if note_density_list:
        print(f"  - Avg note density: {np.mean(note_density_list):.3f}")
        print(f"  - Avg IOI mean: {np.mean(IOI_average_list):.3f}")
        print(f"  - Avg IOI std: {np.mean(IOI_std_list):.3f}")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("midi_dir", type=str, help="directory containing MIDI files")
    args = parser.parse_args()

    analyze_directory(args.midi_dir)