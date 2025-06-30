from pydub import AudioSegment

# Load the audio file
sound = AudioSegment.from_file("1.flac")

# Export to a different format
outputfile = sound.export("test.mp3", format="mp3")