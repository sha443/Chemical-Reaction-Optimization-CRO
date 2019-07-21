from operators import Operators
class Molecule():
    # Variables 
    PE = []             # PE of molecules
    KE = []             # KE of molecules
    numHit = []
    minHit = []
    minPE = []
    minStruct = []
    moleculeTable = None
    moleculeEnergy= None 

    def Mol(self, popSize, InitialKE, other_param):

        # self.moleculeTable = population.GenerateMolecule(prameters here)
        # self.moleculeEnergy = CalculateEnergy(prameters here)
        self.PE = self.moleculeEnergy
        for i in range(len(self.moleculeTable)):
            self.KE.append(initialKE)
            self.numHit.append(0)
            self.minStruct.append(self.moleculeTable[i])
            self.minPE.append(self.moleculeEnergy[i])
            self.minHit.append(0)
        #endfor
    #end
#endclass
