import random
import logging
from midiutil import MIDIFile

# Constants
MELODY_LENGTH = 64
MELODY_VELOCITY = 100
HARMONY_VELOCITY = 70
BASS_VELOCITY = 80
DEFAULT_SCALE = 'minor'
DEFAULT_FILENAME = "generated_music.mid"

# Instrument presets within specified ranges
INSTRUMENT_RANGES = {
    'melody': (0, 31),
    'harmony': (32, 63),
    'bass': (64, 95)
}

# Velocities based on the musical role of each track
VELOCITY_LEVELS = {
    'melody': [80, 100, 110],
    'harmony': [60, 70, 80],
    'bass': [70, 80, 90]
}

class MusicScale:
    """
    Represents a musical scale and provides scale degrees and notes for different scales.
    """

    def __init__(self):
        self.scales = {
            'major': [0, 2, 4, 5, 7, 9, 11],
            'minor': [0, 2, 3, 5, 7, 8, 10],
            'dorian': [0, 2, 3, 5, 7, 9, 10],
            'mixolydian': [0, 2, 4, 5, 7, 9, 10]
            # Add more scales here
        }
        self.notes = ['C', 'D', 'E', 'F', 'G', 'A', 'B']

    def get_scale_degrees(self, scale):
        """
        Get the scale degrees for a given musical scale.
        :param scale: The name of the musical scale.
        :return: List of scale degrees.
        """
        return self.scales.get(scale, [])

class ChordProgressionGenerator:
    """
    Generates chord progressions based on predefined patterns and rules.
    """

    def __init__(self, scales):
        self.chord_progressions = [
            ['I', 'IV', 'V'],
            ['ii', 'V', 'I'],
            ['vi', 'IV', 'I', 'V'],
            ['ii', 'V', 'I', 'IV'],
            ['I', 'iii', 'IV', 'ii', 'V', 'vi']
            # Add more chord progressions here
        ]
        self.chord_symbols_to_degrees = {
            'I': 0, 'ii': 1, 'iii': 2, 'IV': 3, 'V': 4, 'vi': 5, 'vii': 6
        }
        self.scales = scales

    def generate_chord_progression(self, scale):
        """
        Generate a dynamic chord progression.
        :param scale: The musical scale to use.
        :return: A list of chord symbols.
        """
        return random.choice(self.chord_progressions)

    def get_harmonic_notes(self, chord_symbol, scale):
        """
        Get harmonically relevant notes for a given chord symbol and scale.
        :param chord_symbol: The chord symbol.
        :param scale: The musical scale.
        :return: List of harmonic notes.
        """
        chord_degree = self.chord_symbols_to_degrees[chord_symbol]
        scale_degrees = self.scales.get_scale_degrees(scale)
        harmonic_notes = [self.scales.notes[(chord_degree + degree) % len(self.scales.notes)] for degree in
                          scale_degrees]
        return harmonic_notes

class RetroGameMelodyGenerator:
    """
    Generates retro game-style melodic patterns.
    """

    def __init__(self, scale_obj):
        self.scale_obj = scale_obj
        self.chord_progression_generator = ChordProgressionGenerator(self.scale_obj)
        self.note_durations = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]

    def generate_melody(self, chord_progression, scale='major'):
        """
        Generate retro game-style melodic patterns based on chord progressions and a musical scale.
        :param chord_progression: List of chord symbols.
        :param scale: The musical scale to use.
        :return: List of melody notes and durations.
        """
        scale_degrees = self.scale_obj.get_scale_degrees(scale)
        melody = []

        current_degree = random.choice(scale_degrees)
        melody.append(self.scale_obj.notes[current_degree % len(self.scale_obj.notes)])

        for _ in range(MELODY_LENGTH - 1):
            chord_symbol = random.choice(chord_progression)
            chord_degree = self.chord_progression_generator.chord_symbols_to_degrees[chord_symbol]

            available_steps = [1, 2, 3, 4, 5, 6]
            if chord_degree in [0, 3, 4, 6]:
                available_steps.extend([6, 7, 8])
            step = random.choice(available_steps)

            current_degree = (current_degree + step) % len(scale_degrees)

            note_duration = random.choice(self.note_durations)

            melody.append((self.scale_obj.notes[current_degree], note_duration))

        return melody

class RetroGameHarmonyGenerator:
    """
    Generates retro game-style harmonic patterns.
    """

    def __init__(self, scale_obj):
        self.scale_obj = scale_obj
        self.chord_progression_generator = ChordProgressionGenerator(self.scale_obj)

    def generate_harmony(self, melody, chord_progression, scale):
        """
        Generate retro game-style harmonic patterns based on melody and chord progressions.
        :param melody: List of melody notes and durations.
        :param chord_progression: List of chord symbols.
        :param scale: The musical scale to use.
        :return: List of harmony notes and durations.
        """
        harmonic_notes = []
        for chord_symbol in chord_progression:
            chord_notes = self.chord_progression_generator.get_harmonic_notes(chord_symbol, scale)
            harmonic_notes.extend(chord_notes)

        harmony = [
            (harmonic_notes[(self.scale_obj.notes.index(note[0]) + 2) % len(harmonic_notes)], 0.25)
            if isinstance(note, tuple) else (note, 0.25)
            for note in melody
        ] + [
            (harmonic_notes[(self.scale_obj.notes.index(note[0]) + 4) % len(harmonic_notes)], 0.25)
            if isinstance(note, tuple) else (note, 0.25)
            for note in melody
        ]
        return harmony

class RetroGameMidiGenerator:
    """
    Generates retro game-style MIDI data based on notes, durations, and velocities.
    """

    def __init__(self, note_to_midi, duration):
        self.note_to_midi = note_to_midi
        self.duration = duration

    def add_notes_to_midi(self, midi, notes, time, track=0):
        """
        Add retro game-style notes to the MIDI file.
        :param midi: The MIDIFile instance.
        :param notes: List of notes with velocities and durations.
        :param time: Current time in the MIDI timeline.
        :param track: The MIDI track to add notes to.
        """
        for note, velocity, dur in notes:
            if note in self.note_to_midi:
                midi.addNote(track, 0, self.note_to_midi[note], time, dur, velocity)
                time += dur

class RetroGameBassGenerator:
    """
    Generates retro game-style bass lines.
    """

    def __init__(self, scale_obj):
        self.scale_obj = scale_obj

    def generate_bass(self, melody, scale):
        scale_degrees = self.scale_obj.get_scale_degrees(scale)
        bass = []

        for note, duration in melody:
            if isinstance(note, tuple):
                note_degree = self.scale_obj.notes.index(note[0])
                bass_note_degree = (note_degree - 9) % len(scale_degrees)
                bass_note = self.scale_obj.notes[scale_degrees[bass_note_degree]]
                bass.append((bass_note, duration))
            else:
                bass.append((note, duration))

        return bass

class RetroGameMusicGenerator:
    """
    Generates retro game-style music compositions.
    """

    def __init__(self, scale=DEFAULT_SCALE, filename=DEFAULT_FILENAME):
        self.note_to_midi = {'C': 60, 'D': 62, 'E': 64, 'F': 65, 'G': 67, 'A': 69, 'B': 71}
        self.duration = 0.25
        self.tempo = 120
        self.scale_obj = MusicScale()
        self.scale = scale
        self.filename = filename
        self.chord_progression_generator = ChordProgressionGenerator(self.scale_obj)

    def generate_music(self):
        """
        Generate retro game-style melody, harmony, and bass lines using enhanced rules.
        :return: Melody, harmony, and bass lists.
        """
        try:
            chord_progression = self.chord_progression_generator.generate_chord_progression(self.scale)
            melody_generator = RetroGameMelodyGenerator(self.scale_obj)
            melody = melody_generator.generate_melody(chord_progression, self.scale)

            melody = [(note, self.duration) if isinstance(note, str) else note for note in melody]

            harmony_generator = RetroGameHarmonyGenerator(self.scale_obj)
            harmony = harmony_generator.generate_harmony(melody, chord_progression, self.scale)

            bass_generator = RetroGameBassGenerator(self.scale_obj)
            bass = bass_generator.generate_bass(melody, self.scale)

            return melody, harmony, bass
        except Exception as e:
            logging.error("An error occurred during music generation:", exc_info=True)
            return None, None, None

    def save_to_midi(self, melody, harmony, bass):
        """
        Save generated retro game-style music to a MIDI file.
        :param melody: Melody notes and durations.
        :param harmony: Harmony notes and durations.
        :param bass: Bass notes and durations.
        """
        try:
            midi = MIDIFile(3)
            time = 0

            midi_generator = RetroGameMidiGenerator(self.note_to_midi, self.duration)

            melody_notes = [
                (note, MELODY_VELOCITY, dur) for note, dur in melody
            ]
            harmony_notes = [
                (note, HARMONY_VELOCITY, dur) for note, dur in harmony
            ]
            bass_notes = [
                (note, BASS_VELOCITY, dur) for note, dur in bass
            ]

            midi_generator.add_notes_to_midi(midi, melody_notes, time, track=0)
            time = sum(dur for _, _, dur in melody_notes)
            midi_generator.add_notes_to_midi(midi, harmony_notes, time, track=1)
            time = sum(dur for _, _, dur in harmony_notes)
            midi_generator.add_notes_to_midi(midi, bass_notes, time, track=2)

            with open(self.filename, "wb") as output_file:
                midi.writeFile(output_file)
        except Exception as e:
            logging.error("An error occurred while saving MIDI:", exc_info=True)

# Configure logging
logging.basicConfig(filename='app.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Main program
if __name__ == "__main__":
    generator = RetroGameMusicGenerator()
    melody, harmony, bass = generator.generate_music()

    if melody is not None and harmony is not None and bass is not None:
        generator.save_to_midi(melody, harmony, bass)
        print("Generated retro game-style music saved to", generator.filename)
