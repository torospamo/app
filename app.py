import streamlit as st
import random

st.set_page_config(page_title="Generator LRK", page_icon="🥁", layout="centered")

# --- Styl ---
st.markdown("""
    <style>
        .stApp {
            background-color: #101010;
            color: white;
            text-align: center;
        }
        .litera {
            display: inline-block;
            font-weight: bold;
            font-size: 36px;
            margin: 0 6px;
        }
        .litera.L { color: #3ba4ff; }
        .litera.R { color: #4aff3b; }
        .litera.K { color: #ff4a4a; }
    </style>
""", unsafe_allow_html=True)

st.markdown("<h2>🎵 Generator sekwencji L R K</h2>", unsafe_allow_html=True)

# --- Ustawienia ---
dostepne_dlugosci = [3, 4, 5, 6, 8, 12, 16]
dlugosc = st.selectbox("Długość sekwencji:", dostepne_dlugosci, index=5)

st.markdown("### Ustawienia ilości liter (min / max)")

# --- Formularz min/max ---
minL = st.number_input("Min L", min_value=0, max_value=dlugosc, value=2)
maxL = st.number_input("Max L", min_value=minL, max_value=dlugosc, value=2)
minR = st.number_input("Min R", min_value=0, max_value=dlugosc, value=2)
maxR = st.number_input("Max R", min_value=minR, max_value=dlugosc, value=2)
minK = st.number_input("Min K", min_value=0, max_value=dlugosc, value=2)
maxK = st.number_input("Max K", min_value=minK, max_value=dlugosc, value=2)

# --- Funkcja korekty ---
def popraw_zakresy(dlugosc, miny, maxy):
    suma_min = sum(miny.values())
    suma_max = sum(maxy.values())

    # Korekta jeśli suma_min > długość
    if suma_min > dlugosc:
        wsp = dlugosc / suma_min
        for k in miny:
            miny[k] = max(0, int(miny[k] * wsp))

    # Korekta jeśli suma_max < długość
    if suma_max < dlugosc:
        wsp = dlugosc / suma_max if suma_max > 0 else 1
        for k in maxy:
            maxy[k] = min(dlugosc, int(maxy[k] * wsp))

    return miny, maxy

# --- Generowanie sekwencji ---
def generuj_sekwencje(dlugosc, miny, maxy):
    miny, maxy = popraw_zakresy(dlugosc, miny, maxy)
    litery = []
    for l in "LRK":
        litery.extend([l] * miny[l])

    while len(litery) < dlugosc:
        los = random.choice("LRK")
        if litery.count(los) < maxy[los]:
            litery.append(los)
        elif all(litery.count(x) >= maxy[x] for x in "LRK"):
            break

    random.shuffle(litery)
    return litery

# --- Obsługa przycisku ---
if st.button("🎲 Generuj sekwencję"):
    miny = {"L": minL, "R": minR, "K": minK}
    maxy = {"L": maxL, "R": maxR, "K": maxK}
    seq = generuj_sekwencje(dlugosc, miny, maxy)
    html = "".join([f"<span class='litera {l}'>{l}</span>" for l in seq])
    st.markdown(html, unsafe_allow_html=True)

st.markdown("<hr><small>by ChatGPT & Użytkownik 🎧</small>", unsafe_allow_html=True)