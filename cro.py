import random
import math
from operators import Operators
class CRO():

	######################################################################
	# OnWall Ineffective Colision handler
	######################################################################
	def OnwallIneffectiveCollision(self,mole,oldMol, index):
		operator = Operators()
		newMol = operator.OnWall(oldMol)
		PEnew = CRO().CalculateEnergy(mole,newMol)
		KEnew = 0.0
		mole.numHit[index] = mole.numHit[index] + 1
		t = mole.PE[index] + mole.KE1[index]
		if (t>=PEnew):
			a = (random.uniform(0,1) * (1-self.KELossRate))+self.KELossRate
			KEnew = (mole.PE[index] - PEnew + mole.KE1[index])*a
			mole.moleculeTable[index] = newMol
			mole.PE[index] = PEnew
			mole.KE1[index] = KEnew

			# Online update
			if(mole.PE[index]<mole.minPE[index]):
				mole.minStruct[index] = mole
				mole.minPE[index] = mole.PE[index]
				mole.minHit[index] = mole.numHit[index]
			#endif
		#endif
	#end function

	######################################################################
	# Decomposition handler
	######################################################################
	def Decomposition(self,mole,oldMol,index):
		operator = Operators()
		newMol1, newMol2 = operator.Decomposition(oldMol)
		pe1 = CRO().CalculateEnergy(mole,newMol1)
		pe2 = CRO().CalculateEnergy(mole,newMol2)

		e_dec = 0
		gamma1 = 0
		gamma2 = 0
		gamma3 = 0
		gamma1 = random.uniform(0,1)
		gamma2 = random.uniform(0,1)

		if ((mole.PE[index] + mole.KE1[index]) >= (pe1+pe2)):
			e_dec = (mole.PE[index] + mole.KE1[index]) - (pe1 + pe2)
		else:
		   e_dec = (mole.PE[index] + mole.KE1[index]) + gamma1 * gamma2 * self.buffer - (pe1 + pe2)
		# endif

		if (e_dec>=0):
		   self.buffer = self.buffer * (1 -( gamma1*gamma2))
		   gamma3 = random.uniform(0,1)

		   mole.moleculeTable[index] = newMol1
		   mole.PE[index] = pe1
		   mole.KE1[index] = e_dec * gamma3
		   mole.numHit[index] = 0
		   mole.minHit[index] = 0
		   mole.minStruct[index] = newMol1
		   mole.minPE[index] = pe1

		   mole.moleculeTable.append(newMol2)
		   mole.PE.append(pe2)
		   mole.KE1.append(e_dec * gamma3)
		   mole.numHit.append(0)
		   mole.minHit.append(0)
		   mole.minStruct.append(newMol2)
		   mole.minPE.append(pe2)

		else:
		   mole.numHit[index] = mole.numHit[index] + 1
		# endif
	# end function

	######################################################################
	# IntermolecularIneffectiveCollision handler
	######################################################################
	def IntermolecularIneffectiveCollision(self,mole,oldMol1,oldMol2,index1,index2):
		operator = Operators()
		newMol1, newMol2 = operator.Intermolecular(oldMol1, oldMol2)
		pe1 = CRO().CalculateEnergy(mole,newMol1)
		pe2 = CRO().CalculateEnergy(mole,newMol2)
		
		e_inter = 0
		gamma4 = random.uniform(0,1)

		mole.numHit[index1] = mole.numHit[index1] + 1
		mole.numHit[index2] = mole.numHit[index2] + 1
		e_inter = (mole.PE[index1] + mole.PE[index2] + mole.KE1[index1] + mole.KE1[index2]) - (pe1 + pe2)
		if (e_inter>=0):
			mole.moleculeTable[index1] = newMol1
			mole.moleculeTable[index2] = newMol2
			mole.PE[index1] = pe1
			mole.PE[index2] = pe2
			mole.KE1[index1] = e_inter * gamma4
			mole.KE1[index2] = e_inter * (1 - gamma4)
			
			# Online update
			if (mole.PE[index1]<mole.minPE[index1]):
				mole.minStruct[index1] = mole.moleculeTable[index1]
				mole.minPE[index1] = mole.PE[index1]
				mole.minHit[index1] = mole.numHit[index1]
			# endif

			if (mole.PE[index2]<mole.minPE[index2]):
				mole.minStruct[index2] = mole.moleculeTable[index2]
				mole.minPE[index2] = mole.PE[index2]
				mole.minHit[index2] = mole.numHit[index2]
			# endif
		# endif
	# end function

	######################################################################
	# Synthesis handler
	######################################################################
	def Synthesis (self,mole,oldMol1,oldMol2,index1,index2):
		operator = Operators()
		newMol = operator.Synthesis(oldMol1, oldMol2)
		pe_new = CRO().CalculateEnergy(mole,newMol)

		if((mole.PE[index1]+mole.PE[index2] + mole.KE1[index1]+mole.KE1[index2])>=pe_new):
			
			ke_new = (mole.PE[index1] + mole.PE[index2] + mole.KE1[index1] + mole.KE1[index2]) - pe_new

			del mole.moleculeTable[index1]
			del mole.PE[index1]
			del mole.KE1[index1]
			del mole.numHit[index1]
			del mole.minHit[index1]
			del mole.minStruct[index1]
			del mole.minPE[index1]

			if(index2>=index1):
				# position of index2 is decreased by 1
				index2 = index2 -1

			del mole.moleculeTable[index2]
			del mole.PE[index2]
			del mole.KE1[index2]
			del mole.numHit[index2]
			del mole.minHit[index2]
			del mole.minStruct[index2]
			del mole.minPE[index2]

			mole.moleculeTable.append(newMol)
			mole.PE.append(pe_new)
			mole.KE1.append(ke_new)
			mole.numHit.append(0)
			mole.minHit.append(0)
			mole.minStruct.append(newMol)
			mole.minPE.append(pe_new)
		else:
			mole.numHit[index1] = mole.numHit[index1] + 1
			mole.numHit[index1] = mole.numHit[index1] + 1
		# endif
	# end function

	######################################################################
	# Main CRO handler
	######################################################################
	def CRO(self,popSize, KELossRate, MoleColl, InitialKE, alpha, beta, buffer, mole,iteration):
		b = 0
		i = 0
		w = None
		oldMol1 = None
		oldMol2 = None
		index, index1, index2 = 0,0,0
		minEnrg = 1000
		sl=0

		for j in range(len(mole.PE)):
			if (mole.PE[j] < minEnrg):
				minEnrg = mole.PE[j]
				sl = j+1
			#endif
		#endfor

		# Oprators hit counter
		on = 0
		dec = 0
		inef = 0
		syn = 0

		# Main iteration starts
		for i in range(iteration):

			b = random.uniform(0,1)
			# Unimolecular or intermolecular decision
			if (b>MoleColl):
				index = random.randint(0, len(mole.KE1)-1)
				# Decomposition or OnwallIneffectiveCollision decision
				if ((mole.numHit[index]-mole.minHit[index])>alpha):
					dec+=1
					CRO().Decomposition(mole,mole.moleculeTable[index], index)
				#endif
				else:
					on+=1
					CRO().OnwallIneffectiveCollision(mole,mole.moleculeTable[index], index)
				#end else
			#endif

			
			else:
				index1 = random.randint(0, len(mole.KE1)-1)
				index2 = random.randint(0, len(mole.KE1)-1)
				# Synthesis or IntermolecularIneffectiveCollision decision
				if ((mole.KE1[index1]+mole.KE1[index2])<beta):
					syn+=1
					CRO().Synthesis(mole,mole.moleculeTable[index1], mole.moleculeTable[index2], index1, index2)
				#endif
				else:
					inef+=1
					CRO().IntermolecularIneffectiveCollision(mole, mole.moleculeTable[index1], mole.moleculeTable[index2], index1, index2)
				#endelse
			#end else
		# Endfor iteration
		
		# Finding minimum energy
		minEnrg = math.inf
		mole.PE = mole.PE
		minEnrgIndex = None


		for j in range(len(mole.PE)):
			if (mole.PE[j]<minEnrg):
				minEnrg = mole.PE[j]
				minEnrgIndex = j
			#endif
		#endfor
		hits = "Onwall= "+str(on) +"\tDec = "+str(dec)+"\tSyn = "+str(syn)+"\tIntermolecular = "+str(inef)+"\n"
		
		# Logs:
		print(hits, minEnrg, minEnrgIndex)

		return minEnrg, minEnrgIndex

	#end function
	def CalculateEnergy(self,mole,w):
		energy = 0
		# Calculate your own PE here
		return energy
	# end function

# End class