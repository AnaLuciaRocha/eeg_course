# EEG workshop: cleaning brain signals with MNE-Python

Notebooks (PT-PT) for a non-technical audience on **removing artifacts from EEG**.
They are made to run on **Google Colab**: upload a notebook (File → Upload notebook) and use Runtime → Run all.

```
notebooks/01_remocao_artefactos.ipynb   the workshop: filtering, a broken electrode, removing blinks with ICA
notebooks/01_artifact_removal.ipynb     same workshop notebook in English
notebooks/02_pipeline_completo.ipynb    full automatic pipeline for your own recordings
scripts/prepare_data.py                 pre-computes filtering + ICA locally (not used on Colab)
data/                                   local data folders (see data/README.md)
```

## Workshop notebook (`01_remocao_artefactos.ipynb`)

Uses a public recording ([PhysioNet EEG Motor Movement/Imagery](https://physionet.org/content/eegmmidb/1.0.0/), downloaded automatically).
Everything is computed live; ICA takes a few seconds.

## Full pipeline (`02_pipeline_completo.ipynb`)

1. Upload your recordings with the **Choose Files** button (or Cancel to use the example data).
2. Line-noise notch (50/60 Hz, auto-detected) → 1 Hz high-pass → bad-channel detection (PREP criteria, `pyprep`) and interpolation → average reference → extended-infomax ICA → automatic component labelling (ICLabel, `mne-icalabel`) → removal of eye/muscle/heart/line-noise/channel-noise components → 40 Hz low-pass.
3. Results are downloaded as a `.zip`: cleaned recording (`_clean-raw.fif`), ICA (`-ica.fif`) and an HTML report (`_relatorio.html`).

## Local development

`poetry install`, then `poetry run jupyter lab`. The notebooks target Colab (e.g. `google.colab.files` for upload/download), so the upload/download cells only work there.
