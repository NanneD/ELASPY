![ELASPY logo](doc/_static/ELASPY_light.svg)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

# ELASPY

ELASPY (Electric Ambulance Simulator Python) is a discrete-event simulator of the emergency response process of electric and diesel ambulances built in Python. For more information, please visit the ELASPY website: https://nanned.github.io/ELASPY.

The code is written in Python 3.10.8.

## Installation

For installation instructions, please see: https://nanned.github.io/ELASPY/installation/installation.html.

## Documentation

For the user guide, including documentation and a quickstart, please see: https://nanned.github.io/ELASPY/user_guide/userguide.html.

## Citing

If you would like to cite ``ELASPY``, please consider citing the following paper:
> Nanne A. Dieleman, Caroline J. Jagtenberg (2024).
> Electric ambulances: will the need for charging affect response times?
> Preprint available at SSRN: https://ssrn.com/abstract=4874479. doi: 10.2139/ssrn.4874479.

Or, using the following BibTeX entry:

```bibtex
@article{Dieleman_Jagtenberg_2024,
	title = {Electric ambulances: will the need for charging affect response times?},
	author = {Dieleman, Nanne A. and Jagtenberg, Caroline J.},
	year = {2024},
        url = {https://ssrn.com/abstract=4874479},
	doi = {10.2139/ssrn.4874479},
}
```

## License

The GNU General Public License v3 (GPL-3) license is used. For more information, please see the included LICENSE.md file.

## Contributing

If you would like to contribute to ``ELASPY`` in any way, please feel free to create an [issue](https://github.com/NanneD/ELASPY/issues) to discuss what you would like to add or change. Moreover, make sure that your code submission includes:
- tests
- type hints
- documentation
- docstrings for the added/changed methods, classes, etc. according to the NumPy docstrings format

To check whether the type hints and tests run smoothly, you can follow these steps:
1. Open the command line and move to the ``ELASPY`` folder.
2. Run the tests by using the following command:
```
pytest elaspy/tests.py
```
3. Run the mypy checker by using:
```
mypy elaspy/
```