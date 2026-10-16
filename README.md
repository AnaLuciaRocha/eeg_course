# EEG workshop: cleaning brain signals with MNE-Python

Notebooks (PT-PT) for a non-technical audience on **removing artifacts from EEG**.

## Getting started

### On Google Colab (used in the workshop)

Upload a notebook (**File → Upload notebook**) and use **Runtime → Run all**. Nothing to install:
the first cell installs the libraries and the example data is downloaded automatically.

### Locally

```bash
poetry install                 # needs Python 3.13–3.15
poetry run jupyter lab         # then open the notebooks in notebooks/
```

The same notebooks run in local Jupyter; the differences are handled in the hidden setup cells:

- **Example data** is downloaded automatically from PhysioNet on the first run (into `data/raw/`; needs internet once).
- **Your own recordings**: copy them into `data/raw/`. The pipeline uses them instead of the Colab upload button.
- **Results** are saved to `data/preprocessed/` (instead of a browser download).

## Contents

```
notebooks/01_remocao_artefactos.ipynb   the workshop: filtering, a broken electrode, removing blinks with ICA
notebooks/01_artifact_removal.ipynb     same workshop notebook in English
notebooks/02_pipeline_completo.ipynb    full automatic pipeline for your own recordings
scripts/eeg_viwer.py                    local EEG viewer: pick a file and inspect it in the MNE browser
data/                                   local data folders (see data/README.md)
```

## Workshop notebook (`01_remocao_artefactos.ipynb`)

Uses a public recording ([PhysioNet EEG Motor Movement/Imagery](https://physionet.org/content/eegmmidb/1.0.0/), downloaded automatically).
Everything is computed live; ICA takes a few seconds.

## Full pipeline (`02_pipeline_completo.ipynb`)

1. Upload your recordings with the **Choose Files** button (or Cancel to use the example data).
2. Line-noise notch (50/60 Hz, auto-detected) → 1 Hz high-pass → bad-channel detection (PREP criteria, `pyprep`) and interpolation → average reference → extended-infomax ICA → automatic component labelling (ICLabel, `mne-icalabel`) → removal of eye/muscle/heart/line-noise/channel-noise components → 40 Hz low-pass.
3. Results are downloaded as a `.zip`: cleaned recording (`_clean-raw.fif`), ICA (`-ica.fif`) and an HTML report (`_relatorio.html`).

## Viewing recordings locally

```bash
poetry run python scripts/eeg_viwer.py              # pick a file in a dialog (starts in data/)
poetry run python scripts/eeg_viwer.py file.edf     # open a file directly
```

Opens the recording in MNE's interactive browser (1-40 Hz display filter). Clinical channel names
(`EEG Fp1-REF`, `T3`, ...) are matched to standard positions, as in the pipeline. Press `?` in the browser for shortcuts.
Works for raw files in `data/raw/` and pipeline output in `data/preprocessed/` (`*_clean-raw.fif`).
