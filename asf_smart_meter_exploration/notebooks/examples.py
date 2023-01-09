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
from asf_smart_meter_exploration.getters.get_processed_data import (
    get_meter_data,
)
from asf_smart_meter_exploration.analysis.inertia_plots import produce_inertia_plots
from asf_smart_meter_exploration.analysis.clustering import (
    cluster_and_plot_all_variants,
)

# %% [markdown]
# ## Examples

# %% [markdown]
# Get processed meter data (if processed file is not present, this will process the raw data which takes ~15 mins):

# %%
get_meter_data()

# %% [markdown]
# Produce inertia plots for all clustering variants (results can be seen in `outputs/figures/inertia/`):

# %%
produce_inertia_plots()

# %% [markdown]
# Run clustering and plot results for all variants (results can be seen in `outputs/figures/clusters/`):

# %%
cluster_and_plot_all_variants()

# %%
