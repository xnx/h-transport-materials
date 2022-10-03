import h_transport_materials as htm
from h_transport_materials import (
    ArrheniusProperty,
    Solubility,
    diffusivities,
    solubilities,
)
import h_transport_materials.conversion as c
import numpy as np

GOLD_MOLAR_VOLUME = 1.02e-5  # m3/mol https://www.aqua-calc.com/calculate/mole-to-volume-and-weight/substance/gold

# TODO fit it ourselves  https://www.degruyter.com/document/doi/10.1515/zna-1962-0415/html
eichenauer_diffusivity = ArrheniusProperty(
    pre_exp=5.60e-8,
    act_energy=c.kJ_per_mol_to_eV(23.6),
    range=(773, 1273),
    source="eichenauer_messung_1962",
    isotope="H",
)


# NOTE: this was computed from the permeability of Caskey and Derrick and the diffusivity of Eichenauer
shimada_solubility = Solubility(
    units="m-3 Pa-1/2",
    pre_exp=7.8e1 * htm.avogadro_nb,
    act_energy=c.kJ_per_mol_to_eV(99.4),
    range=(773, 873),
    source="shimada_608_2020",
    isotope="H",
)

data_T_mclellan = np.array(
    [
        1050.0,
        997.0,
        948.0,
        939.0,
        910.0,
        878.0,
        838.0,
        805.0,
        793.0,
        777.0,
        735.0,
        693.0,
    ]
)  # degC Table1
data_T_mclellan += 273.15  # in Kelvin

data_y_mclellan = (
    np.array([2.86, 2.51, 2.23, 1.93, 1.96, 1.96, 1.66, 1.66, 1.66, 1.30, 1.27, 1.06])
    * 1e-6
)  # in at.fr. Table 1
data_y_mclellan *= htm.avogadro_nb / GOLD_MOLAR_VOLUME  # in H m-3 Pa-1/2

mclellan_solubility = Solubility(
    data_T=data_T_mclellan,
    data_y=data_y_mclellan,
    units="m-3 Pa-1/2",
    source="mclellan_solid_1973",
    isotope="H",
)


gold_diffusivities = [eichenauer_diffusivity]

gold_solubilities = [shimada_solubility, mclellan_solubility]

for prop in gold_diffusivities + gold_solubilities:
    prop.material = "gold"

diffusivities.properties += gold_diffusivities
solubilities.properties += gold_solubilities
