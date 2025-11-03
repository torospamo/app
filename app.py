import customtkinter as ctk
import random

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Generator sekwencji L R K")
app.geometry("420x520")
app.minsize(360, 440)

dostepne_dlugosci = [3, 4, 5, 6, 7, 8, 12, 16]
dlugosc_var = ctk.IntVar(value=8)
min_vars = {lit: ctk.IntVar(value=2) for lit in "LRK"}
max_vars = {lit: ctk.IntVar(value=2) for lit in "LRK"}

kolory = {"L": "#3ba4ff", "R": "#4aff3b", "K": "#ff4a4a"}
pola_entry = {}

def popraw_zakresy():
    dl = dlugosc_var.get()

    # Upewnij się, że każda wartość jest w zakresie
    for lit in "LRK":
        mn, mx = min_vars[lit].get(), max_vars[lit].get()
        mn = max(0, min(mn, dl))
        mx = max(mn, min(mx, dl))
        min_vars[lit].set(mn)
        max_vars[lit].set(mx)

    # Dostosuj sumy logicznie
    suma_min = sum(min_vars[l].get() for l in "LRK")
    suma_max = sum(max_vars[l].get() for l in "LRK")

    # Jeśli suma minimów przekracza długość sekwencji → zmniejsz proporcjonalnie
    if suma_min > dl:
        wsp = dl / suma_min
        for lit in "LRK":
            min_vars[lit].set(int(min_vars[lit].get() * wsp))

    # Jeśli suma maksów < długość sekwencji → zwiększ proporcjonalnie
    if suma_max < dl:
        wsp = dl / suma_max if suma_max > 0 else 1
        for lit in "LRK":
            max_vars[lit].set(int(max_vars[lit].get() * wsp))

    # Ostateczna korekta – upewnij się, że suma minimów ≤ S ≤ suma maksów
    while sum(min_vars[l].get() for l in "LRK") > dl:
        for lit in "LRK":
            if min_vars[lit].get() > 0:
                min_vars[lit].set(min_vars[lit].get() - 1)
            if sum(min_vars[l].get() for l in "LRK") <= dl:
                break

    while sum(max_vars[l].get() for l in "LRK") < dl:
        for lit in "LRK":
            if max_vars[lit].get() < dl:
                max_vars[lit].set(max_vars[lit].get() + 1)
            if sum(max_vars[l].get() for l in "LRK") >= dl:
                break


def generuj_sekwencje():
    popraw_zakresy()
    dl = dlugosc_var.get()
    litery = []

    # Dodaj wartości minimalne
    for l in "LRK":
        litery.extend([l] * min_vars[l].get())

    # Ustal dostępne litery
    litery_dostepne = [l for l in "LRK" if max_vars[l].get() > min_vars[l].get()]

    # Dopełnij do pełnej długości
    while len(litery) < dl:
        los = random.choice("LRK")
        if litery.count(los) < max_vars[los].get():
            litery.append(los)
        elif all(litery.count(x) >= max_vars[x].get() for x in "LRK"):
            break

    random.shuffle(litery)

    for widget in wynik_label_frame.winfo_children():
        widget.destroy()

    for lit in litery:
        ctk.CTkLabel(
            wynik_label_frame,
            text=lit,
            text_color=kolory[lit],
            font=("Helvetica", 28, "bold"),
        ).pack(side="left", padx=3)


# --- UI ---
pad_x = 18
ctk.CTkLabel(app, text="Długość sekwencji:", font=("Helvetica", 14)).pack(pady=(18, 6))
dlugosc_menu = ctk.CTkOptionMenu(
    app,
    values=[str(x) for x in dostepne_dlugosci],
    variable=dlugosc_var,
    command=lambda _: popraw_zakresy(),
)
dlugosc_menu.pack(pady=(0, 10))

container = ctk.CTkFrame(app, fg_color="transparent")
container.pack(padx=pad_x, fill="both", expand=False)

tabela = ctk.CTkFrame(container, corner_radius=12)
tabela.pack(pady=12, ipadx=8)

hdr_min = ctk.CTkLabel(tabela, text="Min", font=("Helvetica", 12, "bold"))
hdr_max = ctk.CTkLabel(tabela, text="Max", font=("Helvetica", 12, "bold"))
hdr_min.grid(row=0, column=1, padx=12, pady=(8,6))
hdr_max.grid(row=0, column=2, padx=12, pady=(8,6))

tabela.grid_columnconfigure(0, weight=1)
tabela.grid_columnconfigure(1, weight=1)
tabela.grid_columnconfigure(2, weight=1)

for i, lit in enumerate("LRK", start=1):
    lbl = ctk.CTkLabel(tabela, text=lit, text_color=kolory[lit], font=("Helvetica", 16, "bold"))
    lbl.grid(row=i, column=0, padx=8, pady=6, sticky="nsew")
    entry_min = ctk.CTkEntry(tabela, textvariable=min_vars[lit], width=80, justify="center")
    entry_max = ctk.CTkEntry(tabela, textvariable=max_vars[lit], width=80, justify="center")
    entry_min.grid(row=i, column=1, padx=8, pady=6, sticky="nsew")
    entry_max.grid(row=i, column=2, padx=8, pady=6, sticky="nsew")
    pola_entry[lit] = (entry_min, entry_max)

ctk.CTkButton(app, text="Generuj", command=generuj_sekwencje, height=44, corner_radius=12, font=("Helvetica", 16)).pack(pady=(14, 16))

wynik_label_frame = ctk.CTkFrame(app, fg_color="transparent")
wynik_label_frame.pack(pady=(6, 14))

app.mainloop()