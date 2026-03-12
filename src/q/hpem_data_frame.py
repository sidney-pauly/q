import os
from typing import Any, Callable
import numpy as np
from q.utils.mesh_importer import parse_mesh_file
from q.utils.nam_file_reader import read_nam
from q.utils.pdt_file_reader import read_pdt
from q.utils.reactions import Reaction, Species, parse_reactions_dat_file

class HPEM_DataFrame:
    '''
    Class wrapping input and output data from HPEM.
    All properties are lazy, meaning that the underlying data source (e.g.
    a file) will only be loaded when the data is requested the first time.
    '''

    #region: Backing fields

    _config: dict[str, dict[str, Any]] | None = None

    _mesh: np.ndarray | None = None
    
    _chemical_reactions: tuple[dict[str, Species], list[Reaction]] | None = None

    _data_1d: dict[str, np.ndarray] | None = None

    _data_2d: dict[str, np.ndarray] | None = None

    _iteration_data_1d: dict[str, np.ndarray] | None = None

    _iteration_data_2d: dict[str, np.ndarray] | None = None

    _cycle_data_1d: dict[str, np.ndarray] | None = None

    _cycle_data_2d: dict[str, np.ndarray] | None = None

    #endregion

    #region: Factories

    _config_factory: Callable[..., dict[str, dict[str, Any]]] | None = None

    _mesh_factory: Callable[..., np.ndarray] | None = None

    _chemical_reactions_factory: Callable[..., tuple[dict[str, Species], list[Reaction]]] | None = None

    _data_1d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    _data_2d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    _iteration_data_1d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    _iteration_data_2d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    _cycle_data_1d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    _cycle_data_2d_factory: Callable[..., dict[str, np.ndarray]] | None = None

    #endregion

    #region: properties

    @property
    def config(self):
        '''
        The main configuration for HPEM, usually from the .nam file 
        '''
        
        if self._config is not None:
            return self._config
        
        if self._config_factory is not None:
            self._config = self._config_factory()
        
        return self._config
    
    @config.setter
    def config(self, value: dict[str, dict[str, Any]]):
        self._config = value
        
    @property
    def mesh(self):
        '''
        The mesh of the plasma chamber, usually from initmesh.dat
        '''
        
        if self._mesh is not None:
            return self._mesh
        
        if self._mesh_factory is not None:
            self._mesh = self._mesh_factory()
        
        return self._mesh
    
    @mesh.setter
    def mesh(self, value: np.ndarray):
        self._mesh = value
        
    @property
    def chemical_reactions(self):
        '''
        Chemical reaction data containing species and reaction chains, usually from icp.dat
        '''
        
        if self._chemical_reactions is not None:
            return self._chemical_reactions
        
        if self._chemical_reactions_factory is not None:
            self._chemical_reactions = self._chemical_reactions_factory()
        
        return self._chemical_reactions
    
    @chemical_reactions.setter
    def chemical_reactions(self, value: tuple[dict[str, Species], list[Reaction]]):
        self._chemical_reactions = value

    @property
    def data_1d(self):
        '''
        1d simulation output, usually from TECPLOT_KIN.PDT
        '''
        
        if self._data_1d is not None:
            return self._data_1d
        
        if self._data_1d_factory is not None:
            self._data_1d = self._data_1d_factory()
        
        return self._data_1d
    
    @data_1d.setter
    def data_1d(self, value: dict[str, np.ndarray]):
        self._data_1d = value

    @property
    def data_2d(self):
        '''
        2d simulation output, usually from TECPLOT2D.PDT
        '''
        
        if self._data_2d is not None:
            return self._data_2d
        
        if self._data_2d_factory is not None:
            self._data_2d = self._data_2d_factory()
        
        return self._data_2d
    
    @data_2d.setter
    def data_2d(self, value: dict[str, np.ndarray]):
        self._data_2d = value

    @property
    def iteration_data_1d(self):
        '''
        Same as data_1d, but periodically saved throughout the different iterations of the sim.
        Can be used to check convergence behavior. Usually form movie_icp_1d.pdt
        '''
        
        if self._iteration_data_1d is not None:
            return self._iteration_data_1d
        
        if self._iteration_data_1d_factory is not None:
            self._iteration_data_1d = self._iteration_data_1d_factory()
        
        return self._iteration_data_1d
    
    @iteration_data_1d.setter
    def iteration_data_1d(self, value: dict[str, np.ndarray]):
        self._iteration_data_1d = value

    @property
    def iteration_data_2d(self):
        '''
        Same as data_2d, but periodically saved throughout the different iterations of the sim.
        Can be used to check convergence behavior. Usually form movie_icp.pdt
        '''
        
        if self._iteration_data_2d is not None:
            return self._iteration_data_2d
        
        if self._iteration_data_2d_factory is not None:
            self._iteration_data_2d = self._iteration_data_2d_factory()
        
        return self._iteration_data_2d
    
    @iteration_data_2d.setter
    def iteration_data_2d(self, value: dict[str, np.ndarray]):
        self._iteration_data_2d = value

    @property
    def cycle_data_1d(self):
        '''
        1d simulation data within one frame of the rf cycle (newest iteration). Usually
        from movie1_1d.pdt
        '''
        
        if self._cycle_data_1d is not None:
            return self._cycle_data_1d
        
        if self._cycle_data_1d_factory is not None:
            self._cycle_data_1d = self._cycle_data_1d_factory()
        
        return self._cycle_data_1d
    
    @cycle_data_1d.setter
    def cycle_data_1d(self, value: dict[str, np.ndarray]):
        self._cycle_data_1d = value

    @property
    def cycle_data_2d(self):
        '''
        2d simulation data within one frame of the rf cycle (newest iteration). Usually
        from movie1.pdt
        '''
        
        if self._cycle_data_2d is not None:
            return self._cycle_data_2d
        
        if self._cycle_data_2d_factory is not None:
            self._cycle_data_2d = self._cycle_data_2d_factory()
        
        return self._cycle_data_2d
    
    @cycle_data_2d.setter
    def cycle_data_2d(self, value: dict[str, np.ndarray]):
        self._cycle_data_2d = value

    #endregion

    #region: Factories

    @staticmethod
    def from_files(config_file: str | None = None, mesh_file: str | None = None, chemical_reactions_file: str | None = None, data_1d_file: str | None = None, data_2d_file: str | None = None, iteration_data_1d_file: str | None = None, iteration_data_2d_file: str | None = None, cycle_data_1d_file: str | None = None, cycle_data_2d_file: str | None = None):

        res = HPEM_DataFrame()

        if config_file is not None:
            res._config_factory = lambda : read_nam(config_file)

        if mesh_file is not None:
            res._mesh_factory = lambda : parse_mesh_file(mesh_file)

        if chemical_reactions_file is not None:
            res._chemical_reactions_factory = lambda : parse_reactions_dat_file(chemical_reactions_file)

        if data_1d_file is not None:
            res._data_1d_factory = lambda : read_pdt(data_1d_file)

        if data_2d_file is not None:
            res._data_2d_factory = lambda : read_pdt(data_2d_file)

        if iteration_data_1d_file is not None:
            res._iteration_data_1d_factory = lambda : read_pdt(iteration_data_1d_file)

        if iteration_data_2d_file is not None:
            res._iteration_data_2d_factory = lambda : read_pdt(iteration_data_2d_file)

        if cycle_data_1d_file is not None:
            res._cycle_data_1d_factory = lambda : read_pdt(cycle_data_1d_file)

        if cycle_data_2d_file is not None:
            res._cycle_data_2d_factory = lambda : read_pdt(cycle_data_2d_file)

        return res
    
    @staticmethod
    def from_folder(path: str):
        '''
        Creates an HPEM data frame using the default file names assumed to be located in the folder provided
        '''

        return HPEM_DataFrame.from_files(
            os.path.join(path, 'icp.nam'),
            os.path.join(path, 'initmesh.dat'),
            os.path.join(path, 'icp.dat'),
            os.path.join(path, 'TECPLOT_KIN.PDT'),
            os.path.join(path, 'TECPLOT2D.PDT'),
            os.path.join(path, 'movie_icp_1d.pdt'),
            os.path.join(path, 'movie_icp.pdt'),
            os.path.join(path, 'movie1_1d.pdt'),
            os.path.join(path, 'movie1.pdt'),
        )

    #endregion