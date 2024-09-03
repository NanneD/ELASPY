:html_theme.sidebar_secondary.remove:

ELASPY
======

| **Release** |release|
| **Date** |today|

ELASPY (Electric Ambulance Simulator Python) is a discrete-event simulator of the emergency response process of electric and diesel ambulances. It is built with Python.

With this simulator, you can analyze the impact of transferring from diesel to electric vehicles. The simulator is developed for urgent patient transport. During a simulation run, patients arrive to which ambulances respond by driving to the patient's site and providing on-site treatment. Afterwards, the patient may or may not have to be brought to the hospital by the ambulance, after which the ambulance returns to its base. For more details on the simulation process, please see the paper by `Dieleman and Jagtenberg <https://ssrn.com/abstract=4874479>`_.

| **Citing**
| Please see the README.md/CITATION.cff file on the `GitHub repository <https://github.com/NanneD/ELASPY>`_ for a suggested citation.

| **License**

The GNU General Public License v3 (GPL-3) license is used. For more information, please see the `GitHub repository <https://github.com/NanneD/ELASPY>`_.

| **Contributing**
| Please see the README file on the `GitHub repository <https://github.com/NanneD/ELASPY>`_ for information on how to contribute.

.. grid:: 1 2 2 4

    .. grid-item-card::
	:link: installation
        :link-type: ref
        :link-alt: Installation
        :img-background: _static/Installation_logo.svg

    .. grid-item-card::
        :link: userguide
        :link-type: ref
        :link-alt: User guide
        :img-background: _static/Userguide_logo.svg

    .. grid-item-card::
        :link: api
        :link-type: ref
        :link-alt: API reference
        :img-background: _static/API_logo.svg

    .. grid-item-card::
        :link: releases
        :link-type: ref
        :link-alt: Releases
        :img-background: _static/Releases_logo.svg

.. toctree::
   :hidden:

   installation/installation
   user_guide/userguide
   api/api
   releases/releases
