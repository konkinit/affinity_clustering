<h1 align="center">
    Affinity Clustering 
    <br/>
</h1>

<p align="center">
    The project leverages the distributed framework to implements Affinity Clustering, a hierarchical clustering method, at scale 
    <br/> 
</p>


<p align="center">
    <img alt="Licence" src="https://img.shields.io/bower/l/MI?style=for-the-badge">
    <br/>
    <img alt="Repo size" src="https://img.shields.io/github/repo-size/konkinit/affinity_clustering?style=for-the-badge">
    <a href="https://www.python.org/downloads/release/python-3100/" target="_blank">
        <img src="https://img.shields.io/badge/python-3.10-blue.svg?style=for-the-badge" alt="Python Version"/>
    </a>
    <img alt="Code Style" src="https://img.shields.io/badge/code%20style-black-black?style=for-the-badge">
</p>

<p align="center">
    <a href="https://fr.overleaf.com/6151584112drdsyxchsryy">
        <img src="https://img.shields.io/badge/Overleaf-47A141?style=for-the-badge&logo=Overleaf&logoColor=white" alt="SOURCE CODE"/> 
    </a>
</p>



## Getting Started

1. Get in an environment with `Spark` installed

2. Install dependencies
```bash
pip install -r requirements.txt
```

3. Load the network datasets (heavy enough to provide in the repo)
```bash
bash load-net-datasets.sh
```

4. Run the notebook `./notebooks/experiments.ipynb`


## Datasets



## Experiments



## Citations

```bib
@inproceedings{NIPS2017_2e1b24a6,
 author = {Bateni, Mohammadhossein and Behnezhad, Soheil and Derakhshan, Mahsa and Hajiaghayi, MohammadTaghi and Kiveris, Raimondas and Lattanzi, Silvio and Mirrokni, Vahab},
 booktitle = {Advances in Neural Information Processing Systems},
 editor = {I. Guyon and U. Von Luxburg and S. Bengio and H. Wallach and R. Fergus and S. Vishwanathan and R. Garnett},
 pages = {},
 publisher = {Curran Associates, Inc.},
 title = {Affinity Clustering: Hierarchical Clustering at Scale},
 url = {https://proceedings.neurips.cc/paper_files/paper/2017/file/2e1b24a664f5e9c18f407b2f9c73e821-Paper.pdf},
 volume = {30},
 year = {2017}
}
```
