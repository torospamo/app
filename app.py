import streamlit as st
import random

st.set_page_config(page_title="Generator LRK", page_icon="🎵", layout="centered")

st.markdown("""
    <h2 style='text-align:center; color:white;'>🎵 Generator sekwencji L R K</h2>
""", unsafe_allow_html=True)

# --- Ustawienia stylu ---
st.markdown("""
    <style>
        .stApp {
            background-color: #101010;
        }
        div[data-testid="stNumberInput"] label p {
            color: #cccccc;
        }
        div[data-testid="stNumberInput"] input {
            text-align: center;
            color: black !important;
        }
        .litera {
            display: inline-block;
            font-weight: bold;
            font-size: 32px;
            margin: 0 6px;
        }
    </style>
""", unsafe_allow_html=True)

# --- Dane i zmienne ---
kolory = {"L": "#3ba4ff", "R": "#4aff3b", "K": "#ff4a4a"}
dostepne_dlugosci = [3, 4, 5, 6, 7, 8, 12, 16]

# --- Wybór długości ---
dlugosc = st.selectbox("Długość sekwencji:", dostepne_dlugosci, index=5)

# --- Tabela min/max ---
st.markdown("### Ustawienia ilości liter")
cols_header = st.columns([1, 1, 1, 1])
cols_header[0].write("**Litera**")
cols_header[1].write("**Min**")
cols_header[2].write("**Max**")
cols_header[3].write("")

min_values = {}
max_values = {}

for lit in "LRK":
    cols = st.columns([1, 1, 1, 1])
    cols[0].markdown(f"<span style='color:{kolory[lit]}; font-size:22px; font-weight:bold'>{lit}</span>", unsafe_allow_html=True)
    min_values[lit] = cols[1].number_input(f"min_{lit}", min_value=0, max_value=dlugosc, value=2, key=f"min_{lit}")
    max_values[lit] = cols[2].number_input(f"max_{lit}", min_value=min_values[lit], max_value=dlugosc, value=2, key=f"max_{lit}")

# --- Korekta logiczna ---
def popraw_zakresy():
    Lmin, Rmin, Kmin = min_values["L"], min_values["R"], min_values["K"]
    Lmax, Rmax, Kmax = max_values["L"], max_values["R"], max_values["K"]
    suma_min = Lmin + Rmin + Kmin
    suma_max = Lmax + Rmax + Kmax

    # automatyczna korekta
    if suma_min > dlugosc:
        wsp = dlugosc / suma_min
        Lmin, Rmin, Kmin = int(Lmin * wsp), int(Rmin * wsp), int(Kmin * wsp)
    if suma_max < dlugosc:
        wsp = dlugosc / suma_max if suma_max > 0 else 1
        Lmax, Rmax, Kmax = int(Lmax * wsp), int(Rmax * wsp), int(Kmax * wsp)

    return {"L": [Lmin, Lmax], "R": [Rmin, Rmax], "K": [Kmin, Kmax]}

# --- Generator sekwencji ---
def generuj_sekwencje():
    zakresy = popraw_zakresy()
    litery = []

    for l in "LRK":
        litery.extend([l] * zakresy[l][0])

    while len(litery) < dlugosc:
        los = random.choice("LRK")
        if litery.count(los) < zakresy[los][1]:
            litery.append(los)
        elif all(litery.count(x) >= zakresy[x][1] for x in "LRK"):
            break

    random.shuffle(litery)
    return litery

# --- Przycisk generowania ---
if st.button("🎲 Generuj sekwencję", use_container_width=True):
    sekwencja = generuj_sekwencje()
    wynik_html = "".join([f"<span class='litera' style='color:{kolory[l]}'>{l}</span>" for l in sekwencja])
    st.markdown(f"<div style='text-align:center; margin-top:20px;'>{wynik_html}</div>", unsafe_allow_html=True)

# --- Stopka / informacje ---
st.markdown("""
<hr style="border: 1px solid #333;">
<p style="text-align:center; color:gray; font-size:13px;">
  Aplikacja: <b>Generator LRK</b> • stworzona z pasją 🥁<br>
  Możesz wspomóc rozwój projektu dowolnym datkiem 🙏
</p>
""", unsafe_allow_html=True)