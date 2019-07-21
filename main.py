import os
import sys
from molecule import Molecule
from cro import CRO

class main():
	def __init__(self):
		pass
	def run(self, param):
		
		# Parameters
		iteration = 80
		popSize = 50
		KELossRate= 0.85
		MoleColl= 0.50
		InitialKE= 0
		alpha = 1
		beta = 10
		buffer = 0

		#----------------------------------------------------------------------------------------------
		# Population generation
		#----------------------------------------------------------------------------------------------
		mole = Molecule()
		mole.Mol(popSize, InitialKE,other_param)
		

		#----------------------------------------------------------------------------------------------
		# Optimize with CRO
		#----------------------------------------------------------------------------------------------
		C  = CRO()
		minEnrg, minEnrgIndex = C.CRO(popSize, KELossRate, MoleColl, InitialKE, alpha, beta, buffer, mole,iteration)
	# end function
# end class

#-----------------------------------------------------------------------------------------
# Command line processing area
#-----------------------------------------------------------------------------------------
commandline = sys.argv
main().run(commandline[1])