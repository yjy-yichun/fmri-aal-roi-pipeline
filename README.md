# fMRI ROI Analysis Pipeline (AAL atlas)

This project is a lightweight, reproducible fMRI ROI-level analysis pipeline based on BIDS data and fMRIPrep outputs.

It supports:
- BIDS dataset directory
- fMRIPrep preprocessed outputs in MNI space
- task-based first-level GLM analysis
- ROI extraction using the AAL atlas
- ROI activation comparisons across conditions
- basic visualization (statistical maps and ROI bar plots)
- a simple Streamlit app for interactive inspection

## Project structure
- `fmri_roi_analysis.ipynb`: main notebook
- `streamlit_app.py`: basic Streamlit viewer
- `requirements.txt`: Python dependencies

## Precondition
Before running this pipeline, ensure:
1. You have a valid BIDS-formatted dataset.
2. You have run `fMRIPrep` and generated outputs such as:
   `derivatives/fmriprep/sub-XX/func/sub-XX_task-learning_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz`
3. Each subject has an events file like:
   `sub-XX/func/sub-XX_task-learning_events.tsv`

## Typical directory layout
```text
your_bids_root/
├── sub-01/
│   └── func/
│       ├── sub-01_task-learning_bold.nii.gz
│       ├── sub-01_task-learning_events.tsv
│       └── ...
├── sub-02/
│   └── func/
│       └── ...
├── derivatives/
│   └── fmriprep/
│       └── sub-01/
│           └── func/
│               ├── sub-01_task-learning_space-MNI152NLin2009cAsym_desc-preproc_bold.nii.gz
│               └── ...
```

## Setup
```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Example fMRIPrep command
```bash
docker run --rm -it \
  -v /path/to/BIDS:/data:ro \
  -v /path/to/output:/out \
  -v /path/to/work:/work \
  nipreps/fmriprep:latest /data /out participant \
  --participant-label 01 02 03 \
  --fs-license-file /path/to/license.txt \
  --output-spaces MNI152NLin2009cAsym
```

## Notebook usage
1. Open `fmri_roi_analysis.ipynb`
2. Edit the variables at the top:
   ```python
   bids_root = "/path/to/your/BIDS"
   fmriprep_deriv = "/path/to/your/BIDS/derivatives/fmriprep"
   output_dir = "./results_fmri_roi"
   task_label = "learning"
   ```
3. Run all cells.
4. Results will be saved to `results_fmri_roi`.

## Outputs
- `subject_roi_values.csv`
- `group_roi_stats.csv`
- `group_*_mean_effect.nii.gz`
- plot images in `output_dir`

## Streamlit app
To launch the interactive viewer:
```bash
streamlit run streamlit_app.py
```

This app reads `./results_fmri_roi` and lets you select a task/condition and inspect ROI-wise activation.

## Notes
- This example uses the AAL atlas for ROI segmentation.
- It is designed for ROI-level analysis, not voxel-wise or single-voxel analysis.
- The current notebook performs per-subject first-level GLM plus group ROI statistics.
