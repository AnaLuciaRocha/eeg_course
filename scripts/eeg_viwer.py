"""Abrir um registo de EEG no visualizador interativo do MNE.

Uso (no terminal, na pasta do projeto):

    poetry run python scripts/eeg_viwer.py                   # abre uma janela para escolher o ficheiro
    poetry run python scripts/eeg_viwer.py caminho.edf       # abre diretamente o ficheiro indicado

No visualizador: setas para navegar no tempo, +/- para a escala, clique num canal para o marcar
como inválido, "a" para anotações, "?" para a lista completa de atalhos.
"""

import sys
from pathlib import Path

import mne
import numpy as np
from qtpy.QtWidgets import QApplication, QFileDialog

DATA_DIR = Path(__file__).resolve().parents[1] / "data"
EEG_FILES = "Registos de EEG (*.edf *.bdf *.fif *.set *.vhdr *.cnt *.gdf);;Todos os ficheiros (*)"
MONTAGE = "standard_1005"

# Sufixos de referência habituais em exportações clínicas (ex.: "EEG Fp1-REF", "Fp1-LE", "C3-A1")
REFERENCE_SUFFIXES = {"ref", "le", "av", "avg", "ar", "a1", "a2", "a1a2", "m1", "m2", "linked"}


def choose_file():
    # Janela "Abrir ficheiro", a começar na pasta data/ do projeto
    app = QApplication.instance() or QApplication(sys.argv)
    fname, _ = QFileDialog.getOpenFileName(None, "Abrir registo de EEG", str(DATA_DIR), EEG_FILES)
    return fname


def standard_name(ch, lookup):
    # "EEG FP1-REF" -> "Fp1"; None se o canal não for um único elétrodo do escalpe (ECG, Fp1-F7, ...)
    key = ch.strip(" .").lower()
    for prefix in ("eeg ", "pol "):
        key = key.removeprefix(prefix)
    if "-" in key:
        key, reference = key.split("-", 1)
        if reference.strip() not in REFERENCE_SUFFIXES:
            return None
    return lookup.get(key.strip())


def set_positions(raw):
    # Mesma lógica do notebook 02_pipeline_completo: nomes clínicos -> nomenclatura padrão,
    # posições da montagem padrão, e canais sem posição (ECG, EOG, ...) marcados como auxiliares
    standard = mne.channels.make_standard_montage(MONTAGE)
    lookup = {ch.lower(): ch for ch in standard.ch_names}
    rename = {}
    for ch in raw.ch_names:
        new = standard_name(ch, lookup)
        if new and new != ch and new not in raw.ch_names and new not in rename.values():
            rename[ch] = new
    raw.rename_channels(rename)
    raw.set_montage(standard, on_missing="ignore")
    unknown = [c["ch_name"] for c in raw.info["chs"]
               if c["kind"] == mne.io.constants.FIFF.FIFFV_EEG_CH and np.isnan(c["loc"][:3]).any()]
    raw.set_channel_types({ch: "misc" for ch in unknown})


def has_positions(raw):
    # Verifica se todos os elétrodos de EEG do ficheiro têm uma posição definida no escalpe
    locs = np.array([c["loc"][:3] for c in raw.info["chs"] if c["kind"] == mne.io.constants.FIFF.FIFFV_EEG_CH])
    return locs.size > 0 and not np.isnan(locs).any() and np.abs(locs).sum(axis=1).all()


def main():
    fname = sys.argv[1] if len(sys.argv) > 1 else choose_file()
    if not fname:
        print("Nenhum ficheiro escolhido.")
        return
    raw = mne.io.read_raw(fname, preload=True, verbose="error")
    if not has_positions(raw):
        set_positions(raw)
    print(f"{Path(fname).name}: {len(raw.ch_names)} canais, {raw.times[-1]:.0f} s, {raw.info['sfreq']:.0f} Hz")

    mne.viz.set_browser_backend("qt")
    # Filtro de visualização 1-40 Hz (não altera o ficheiro; pode ser alterado no visualizador).
    # theme="light": fundo branco e sinal preto, independentemente do modo escuro do sistema.
    raw.plot(title=Path(fname).name, highpass=1.0, lowpass=40.0, duration=10, n_channels=30,
             theme="light", block=True)


if __name__ == "__main__":
    main()
