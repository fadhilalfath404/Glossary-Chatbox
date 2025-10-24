import csv
import wikipedia
from wikipedia.exceptions import DisambiguationError, PageError
import warnings
import streamlit as st

#Hide parser warnings#
warnings.filterwarnings("ignore", category=UserWarning, module="wikipedia")

#Set Wikipedia ke Bahasa Indonesia
wikipedia.set_lang("id")

#Load glossary dari CSV#
def load_glossary(file="glossary.csv"):
    glossary = {}
    try:
        with open(file, newline='', encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                glossary[row["term"].strip().lower()] = row["definition"].strip()
    except FileNotFoundError:
        st.error("⚠️ glossary.csv tidak ditemukan. Pastikan file ada di folder yang sama dengan app.py")
    return glossary

#Lookup function: CSV dulu, kalau tidak ada → Wikipedia#
def get_definition(term, glossary):
    key = term.lower().strip()
    if key in glossary:
        return glossary[key]
    try:
        return wikipedia.page(term).summary[:1000]
    except DisambiguationError as e:
        return f"Istilah ambigu. Pilihan: {', '.join(e.options[:5])}"
    except PageError:
        return "Tidak ada halaman yang ditemukan."

#Streamlit UI#
def main():
    st.title("🌦️ Chatbot Glosarium Meteorologi")
    st.write("Apa yang ingin anda ketahui? Saya akan jelaskan.")

    glossary = load_glossary("glossary.csv")

    # Form agar Enter dan tombol sama-sama bisa submit
    with st.form("glossary_form"):
        term = st.text_input(
            "Masukkan istilah:",
            placeholder="contoh: hujan es ❄️"
        )
        submitted = st.form_submit_button("Cari Definisi")

        if submitted:
            if term.strip() == "":
                st.warning("Silakan masukkan istilah.")
            else:
                definition = get_definition(term, glossary)
                st.success(definition)

if __name__ == "__main__":
    main()