import os
import glob
import pandas as pd
import streamlit as st
from nilearn import image, plotting

st.set_page_config(page_title="fMRI ROI Activation Viewer", layout="wide")

output_dir = "./results_fmri_roi"

if not os.path.exists(output_dir):
    st.error(f"Results directory not found: {output_dir}. Please run the notebook first.")
    st.stop()

stats_path = os.path.join(output_dir, "group_roi_stats.csv")
if not os.path.exists(stats_path):
    st.error(f"Missing required file: {stats_path}")
    st.stop()

group_stats = pd.read_csv(stats_path)
conditions = sorted(group_stats["condition"].unique())

st.title("fMRI ROI Activation Viewer (AAL Atlas)")
st.caption("Interactive ROI-level activation inspection from task-based fMRI analysis.")

sel_cond = st.selectbox("Select task/condition", conditions)

df = group_stats[group_stats["condition"] == sel_cond].copy()
df = df.sort_values("p_fdr")

st.subheader(f"ROI stats for {sel_cond}")
st.dataframe(df[["roi_name", "mean_effect", "t", "p_uncorrected", "p_fdr", "significant_fdr"]].head(100))

n_top = st.slider("Show top N ROIs", 5, 50, 10)
top = df.sort_values("mean_effect", key=lambda s: s.abs(), ascending=False).head(n_top)
st.bar_chart(top.set_index("roi_name")["mean_effect"])

map_candidates = glob.glob(os.path.join(output_dir, f"*contrast-{sel_cond}_mean_effect.nii.gz"))
if map_candidates:
    img_path = map_candidates[0]
    st.subheader("Group mean contrast map")
    img = image.load_img(img_path)
    display = plotting.plot_stat_map(img, title=f"Group mean effect: {sel_cond}", threshold=None, display_mode="ortho")
    st.pyplot(display.figure)
else:
    st.info("No group mean effect map found for this condition.")
