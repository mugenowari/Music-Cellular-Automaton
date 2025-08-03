import numpy as np
from mido import Message, MidiFile, MidiTrack

# Conway's Game of Life rules
def game_of_life_step(grid):
    new_grid = grid.copy()
    rows, cols = grid.shape
    for i in range(rows):
        for j in range(cols):
            total = np.sum(grid[max(i-1,0):min(i+2,rows), max(j-1,0):min(j+2,cols)]) - grid[i,j]
            if grid[i,j] == 1:
                if total < 2 or total > 3:
                    new_grid[i,j] = 0
            else:
                if total == 3:
                    new_grid[i,j] = 1
    return new_grid

# Initialize 2D CA grid
rows, cols = 32, 16
grid = np.random.choice([0,1], size=(rows, cols), p=[0.8, 0.2])

# Create MIDI file and track
mid = MidiFile()
track = MidiTrack()
mid.tracks.append(track)

# Map columns to notes (C major scale for example)
scale = [60, 62, 64, 65, 67, 69, 71, 72]  # C D E F G A B C
cols = 32
#note_map = [scale[i % len(scale)] for i in range(cols)]
note_map = [scale[i % len(scale)] + 12 * (i // len(scale)) for i in range(cols)]

# Iterate over each row as a timestep
for timestep in range(rows):
    current_row = grid[timestep]
    for col, cell in enumerate(current_row):
        if cell == 1:
            pitch = note_map[col]
            # Note on
            track.append(Message('note_on', note=pitch, velocity=64, time=0))
            # Note off with short duration
            track.append(Message('note_off', note=pitch, velocity=64, time=120))
    grid = game_of_life_step(grid)

mid.save('game_of_life_polyphonic.mid')
