import streamlit as st
import random
from collections import Counter

st.title("🪄 Hej Nikodem :) - Przetestuj generator podobnych słów (z zachowaniem liter)")

def subtle_mix_preserve(w, max_attempts=10):
    if len(w) < 4:
        return w
    first = w[0]
    last = w[-1]
    middle_orig = list(w[1:-1])
    target_counter = Counter(w)

    attempts = 0
    while attempts < max_attempts:
        middle = middle_orig.copy()
        # delikatne przestawienia: 1-2 zamiany sąsiadów
        for _ in range(random.randint(1, 2)):
            if len(middle) >= 2:
                i = random.randint(0, len(middle)-2)
                middle[i], middle[i+1] = middle[i+1], middle[i]
        candidate = first + ''.join(middle) + last
        if Counter(candidate) == target_counter and candidate != w:
            return candidate
        attempts += 1

    # fallback: zwróć losowe przetasowanie środkowych liter (z zachowaniem liter)
    middle = middle_orig.copy()
    for _ in range(50):
        random.shuffle(middle)
        candidate = first + ''.join(middle) + last
        if Counter(candidate) == target_counter and candidate != w:
            return candidate
    return w  # jeśli nic nie zadziała, zwracamy oryginał

# przykładowe użycie w Streamlit
word = st.text_input("Wpisz słowo:")
if st.button("Generuj"):
    if word:
        st.write(subtle_mix_preserve(word))
    else:
        st.warning("Wpisz słowo.")