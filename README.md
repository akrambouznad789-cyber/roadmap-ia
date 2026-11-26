# AI Roadmap

A public path in artificial intelligence: two 140-day intensive classes, run in parallel, and the projects done before them.

**Site: https://akrambouznad789-cyber.github.io/roadmap-ia/**

## The two classes

| Class | In short | Links |
|---|---|---|
| Applied AI Intensive Class | Building with models: from data up to an open language model served locally, in 9 phases | [route](https://akrambouznad789-cyber.github.io/applied-ai-intensive-class/) · [repository](https://github.com/akrambouznad789-cyber/applied-ai-intensive-class) |
| AI Inference Intensive Class | Running models on your own machine: memory, quantization, serving, up to a private appliance, in 6 phases | [route](https://akrambouznad789-cyber.github.io/ai-inference-intensive-class/) · [repository](https://github.com/akrambouznad789-cyber/ai-inference-intensive-class) |

Both classes move forward on the same day number. A day always follows the same order: theory first (a diagram, a worked numeric example, pseudo-code), an interactive demo, practice that produces a figure or a measurement, then a few sentences on what was understood. Every project aims at a model that runs locally.

## Before the classes

The projects and stations below were done before the two classes; their write-ups are in French.

### Applied projects

Each project is named after its methods; the dataset is only the practical case. Project P4 (BPE tokenization and a mini-Transformer) ends during phase 3 of the Applied AI Intensive Class.

| Project | Question | Methods |
|---|---|---|
| [P1 · Boosting, validation and leakage](projets/P1-boosting-validation/) | At order time, can we predict that a delivery will be late? | Gradient boosting, time-based validation, leakage detection |
| [P2 · Clustering and difference-in-differences](projets/P2-clustering-did/) | Do BIXI stations have usage profiles? Did the Saint-Denis REV bike lane take cyclists away from the Brébeuf path? | k-means, PCA, difference-in-differences |
| [P3 · PyTorch network and embeddings](projets/P3-pytorch-plongements/) | Does a network that learns BIXI trip durations redraw the map of Montreal in its station embeddings? | PyTorch network, embeddings, gradient boosting, time-based validation, local measurement |

### Stations

| Station | Example | Page |
|---|---|---|
| 1 · Neural networks: the multilayer perceptron | Estimating the 30th-highest hourly volume from Québec's public traffic counts | [View](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/01-reseau-neurones/) |
| 2 · Backpropagation and automatic differentiation | A home-made backpropagation engine trains a small network on 200 road sections in Québec, with the same losses as PyTorch | [View](https://akrambouznad789-cyber.github.io/roadmap-ia/parcelles/02-retropropagation/) |

The code of each station is stored in [`archives/stations/`](archives/stations/).

## Repository contents

| Folder | Contents |
|---|---|
| `docs/` | The site: the home page of the two classes and the station pages |
| `projets/` | The applied projects, one folder per project: notebooks, results and README |
| `style/` | The shared figure style |
| `archives/stations/` | The code and results of each station |
| `outils/`, `tests/` | Measurement tools and the checks run on the pages before publishing, with their tests |
| `gabarits/` | The template of the station pages |

## Data

Raw data is not versioned, only results. Each source is credited on the page of its example.
