#!/usr/bin/env python
"""
=============================================
sMRI: Regional Tessellation and Surface Smoothing
=============================================

Introduction
============

This script, tessellation_tutorial.py, demonstrates the use of create_tessellation_flow from nipype.workflows.smri.freesurfer, and it can be run with:

    python tessellation_tutorial.py

This example requires that the user has Freesurfer installed, and that the Freesurfer directory for 'fsaverage' is present.

.. seealso::

	ConnectomeViewer
		The Connectome Viewer connects Multi-Modal Multi-Scale Neuroimaging and Network Datasets For Analysis and Visualization in Python.

	http://www.geuz.org/gmsh/
		Gmsh: a three-dimensional finite element mesh generator with built-in pre- and post-processing facilities

	http://www.blender.org/
		Blender is the free open source 3D content creation suite, available for all major operating systems under the GNU General Public License.

.. warning::

	This workflow will take several hours to finish entirely, since smoothing
    the larger cortical surfaces is very time consuming.

Packages and Data Setup
=======================

Import the necessary modules and workflow from nipype.
"""
import nipype.pipeline.engine as pe          # pypeline engine
import nipype.interfaces.io as nio           # Data i/o
import os, os.path as op
from nipype.workflows.smri.freesurfer import create_tessellation_flow

"""
Directories
===========

Set the default directory and lookup table (LUT) paths
"""

fs_dir = os.environ['FREESURFER_HOME']
lookup_file = op.join(fs_dir,'FreeSurferColorLUT.txt')
subjects_dir = op.join(fs_dir, 'subjects/')
output_dir = './tessellate_tutorial'

"""
Inputs
======

Create the tessellation workflow and set inputs
"""

tessflow = create_tessellation_flow(name='tessflow')
tessflow.inputs.inputspec.subject_id = 'fsaverage'
tessflow.inputs.inputspec.subjects_dir = subjects_dir
tessflow.inputs.inputspec.lookup_file = lookup_file

"""
Outputs
=======

Create a datasink to organize the smoothed meshes
"""

datasink = pe.Node(interface=nio.DataSink(), name="datasink")
datasink.inputs.base_directory = 'meshes'

"""
Execution
=========

Finally, create and run another pipeline that connects the workflow and datasink
"""

tesspipe = pe.Workflow(name='tessellate_tutorial')
tesspipe.base_dir = output_dir
tesspipe.connect([(tessflow, datasink,[('outputspec.meshes', '@meshes.all')])])
tesspipe.run()
