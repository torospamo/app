import streamlit as st
from music21 import stream, note, converter

st.title("Rudyment Generator 🥁")

# Prosty przykład — dwie nuty z LR
pattern = [('L', 'C4'), ('R', 'C4'), ('L', 'C4'), ('R', 'C4')]

s = stream.Stream()
for hand, pitch in pattern:
    n = note.Note(pitch)
    n.quarterLength = 0.25
    n.lyric = hand  # <--- tu pojawia się L lub R pod nutą
    s.append(n)

# Eksport MusicXML do tekstu
xml_str = s.write('musicxml')

# Odczytaj zawartość pliku XML
with open(xml_str, 'r') as f:
    xml_data = f.read()

# Wstaw kod JS z OpenSheetMusicDisplay
osmd_script = f"""
<script src="https://cdn.jsdelivr.net/npm/opensheetmusicdisplay@1.7.6/build/opensheetmusicdisplay.min.js"></script>
<div id="osmd"></div>
<script>
  const osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay("osmd", {{drawingParameters: "compact"}});
  osmd.load(`{xml_data}`).then(() => osmd.render());
</script>
"""

# Wyświetl w Streamlit
st.components.v1.html(osmd_script, height=500, scrolling=True)