# asf_smart_meter_exploration

## Setup

- Meet the data science cookiecutter [requirements](http://nestauk.github.io/ds-cookiecutter/quickstart), in brief:
  - Install: `direnv` and `conda`
- Run `make install` to configure the development environment:
  - Setup the conda environment
  - Configure `pre-commit`

To save plots, follow the instructions [here](https://github.com/altair-viz/altair_saver/#nodejs).

Instructions for downloading data:

- `make inputs-pull` puts a zip file in `/inputs`, script will unzip if not already

## Contributor guidelines

[Technical and working style guidelines](https://github.com/nestauk/ds-cookiecutter/blob/master/GUIDELINES.md)

---

<small><p>Project based on <a target="_blank" href="https://github.com/nestauk/ds-cookiecutter">Nesta's data science project template</a>
(<a href="http://nestauk.github.io/ds-cookiecutter">Read the docs here</a>).
</small>