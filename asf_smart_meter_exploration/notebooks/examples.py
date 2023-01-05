# ---
# jupyter:
#   jupytext:
#     cell_metadata_filter: -all
#     comment_magics: true
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.14.4
#   kernelspec:
#     display_name: asf_smart_meter_exploration
#     language: python
#     name: asf_smart_meter_exploration
# ---

# %% [markdown]
# ## Setup

# %%
import os

os.chdir("../..")

# %%
import pandas as pd

# %%
from asf_smart_meter_exploration import base_config, PROJECT_DIR

from asf_smart_meter_exploration.pipeline.process_raw_data import (
    produce_all_properties_df,
)
from asf_smart_meter_exploration.analysis.inertia_plots import produce_inertia_plots
from asf_smart_meter_exploration.analysis.clustering import (
    cluster_and_plot_all_variants,
)

# %%
meter_data_merged_file_path = PROJECT_DIR / base_config["meter_data_merged_file_path"]

# %% [markdown]
# ## Examples

# %% [markdown]
# Process the raw data to produce half-hourly meter readings for each household (takes ~15 mins):

# %%
produce_all_properties_df()

# %%
pd.read_csv(meter_data_merged_file_path)

# %% [markdown]
# Produce inertia plots for all clustering variants (results can be seen in `outputs/figures/inertia/`):

# %%
produce_inertia_plots()

# %% [markdown]
# Run clustering and plot results for all variants (results can be seen in `outputs/figures/clusters/`):

# %%
cluster_and_plot_all_variants()

# %%
