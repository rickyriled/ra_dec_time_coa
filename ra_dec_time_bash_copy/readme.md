# Creating Injection File:
-------------------------
import sys
import numpy as np
import pylab as pl

import pycbc.waveform
from pycbc.detector import Detector
from pycbc import frame

mass1 = 1.8
mass2 = 1.6
spin1x = 0.0
spin1y = 0.0
spin1z = 0.0
spin2x = 0.0
spin2y = 0.0
spin2z = 0.0
ra = 3.4
dec = 0.5
distance = 10 # Close distance so that the injection can be seen in the data
inclination = 0.2
polarization = 0.3
lambda1 = 0.0
lambda2 = 0.0
coa_phase = 1.1
f_lower = 15
f_ref = 0
approximant = 'IMRPhenomPv2_NRTidalv2'
t = 1264069376


from pycbc.io import FieldArray
from pycbc.inject import InjectionSet

dtype = [('mass1', float), ('mass2', float),
         ('spin1x', float), ('spin2x', float),
         ('spin1y', float), ('spin2y', float),
         ('spin1z', float), ('spin2z', float),
         ('tc', float), ('distance', float),
         ('ra', float), ('dec', float),
         ('approximant', 'S32'), ('f_lower', float),
         ('f_ref', float), ('inclination', float),
         ('coa_phase', float), ('polarization', float),
         ('lambda1', float), ('lambda2', float)]


static_params = {'taper': 'start',
                 'eccentricity': 0.
                 }

num_inj = 1
samples = FieldArray(num_inj, dtype=dtype)

samples['mass1'] = mass1
samples['mass2'] = mass2
samples['spin1x'] = spin1x
samples['spin2x'] = spin2x
samples['spin1y'] = spin1y
samples['spin2y'] = spin2y
samples['spin1z'] = spin1z
samples['spin2z'] = spin2z
samples['tc'] = t
samples['ra'] = ra
samples['dec'] = dec
samples['distance'] = distance
samples['inclination'] = inclination
samples['polarization'] = polarization
samples['f_ref'] = f_ref
samples['f_lower'] = f_lower
samples['coa_phase'] = coa_phase
samples['lambda1'] = 0
samples['lambda2'] = 0
samples['approximant'] = approximant

InjectionSet.write('injection_bright_10.hdf5', samples,
                   static_args=static_params, injtype='cbc',
                   cmd=" ".join(sys.argv))

"pycbc_condition_strain --injection-file injection_{NAME}.hdf5 --channel-name L1:SIM-STRAIN --output-strain-file L-L1_STRAIN-1264068864-1024.gwf --fake-strain-from-file aligo_O4high_extrapolated.txt --fake-strain-seed 100 --low-frequency-cutoff 15 --fake-strain-flow 15 --frame-duration 1024 --gps-start-time 1264068864 --gps-end-time 1264069888 --sample-rate 16384"
