```txt    
        Q   Q   Q                             
  *      \  |  /                               Q
          \ | /   *        
*          \|/        *          Python utility library for the
       *   _|_                   
          /   \                  HYBRID PLASMA EQUIPMENT MODEL
    *     \   /                             (HPEM)
           \ /     *
```


### Why is it called Q?

Buckle up for some lore, I bet this is why you opened this page, to learn about Star Trek, not plasma simulations xD

This is a python package and it deals with plasmas, so we ideally need some kind of plasma snake. Luckily Star Trek has us covered with the [Aldebaran serpent](https://memory-alpha.fandom.com/wiki/Aldebaran_serpent), which is a plasma like three headed
snake. Now "Aldebaran" is a terrible name for a package as everyone would constantly mistype that. Therefore the package is instead named after [Q](https://memory-alpha.fandom.com/wiki/Q) (another Start Trek character) who shape-shifted into an Aldebaran serpent in one episode.

# What it can do (currently)

- Import and Export HPEM files:
    - Result files (`.pdt`)
    - Mesh files (`initmesh.dat`)
    - Chemical reaction data (`icp.dat`)
- Plot HPEM output
    - As 2d plot
    - With geometry
    - As movie
- Analyze chemical reaction data as a network utilizing `networkx`
- Plot chemical reaction data as a graph

# Install

The library can be installed through pip by running 
```
pip install [repository-root]
``` 
(replace `[repository root]` with the actual location fo the downloaded repository).

If you want to install the package in a virtual environment (venv), you can just run the same command from your virtual environment.

## Dependencies

The package currently depends on
- `numpy`:  Used to import HPEM results
- `matplotlib`: required for any plotting methods
- `networkx`: required for graph visualization and graph analysis of chemical processes


