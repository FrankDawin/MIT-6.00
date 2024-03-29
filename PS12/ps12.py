# 6.00 Problem Set 12
#
# Name:
# Collaborators:
# Time:
from __future__ import division
import random
import pylab
import time

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """
#
# PROBLEM 1
#


class SimpleVirus(object):
    """
    Representation of a simple virus (does not model drug effects/resistance).
    """

    def __init__(self, maxBirthProb, clearProb):
        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.        
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """

        virus_random = random.random()
        
        if self.clearProb > virus_random:
            return True

        else:
            return False

    def reproduce(self, popDensity):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).         

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.         
        
        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.               
        """
        # TODO
        # reproduce
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):
            return SimpleVirus(self.maxBirthProb, self.clearProb)
            
        else:
            raise NoChildException()


class SimplePatient(object):
    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses  # is a list, all virus instance
        self.maxPop = maxPop  # an int, max amount of virus in patient
        self.popDensity = self.getTotalPop() / float(self.maxPop)

    def __str__(self):

        print "Viruses len {}".format(len(self.viruses))
        print "maxPop int {}".format(self.maxPop)

        return ""

    def getTotalPop(self):
        """
        Gets the current total virus population. 

        returns: The total virus population (an integer)
        """

        return len(self.viruses)

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
          of virus particles accordingly.

        - The current population density is calculated. This population density
          value is used until the next call to update() 

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.                    

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO

        new_virus = []

        # Check for virus saturation
        assert len(self.viruses) > self.maxPop, "Patient died"

        # Clear viruses from list who died
        for i in self.viruses:
            if i.doesClear() is True:
                self.viruses.remove(i)

        # Verify that viruses remains
        assert len(self.viruses) <= 0, "Patient cured"

        # Pop density calculated
        self.popDensity = self.getTotalPop() / float(self.maxPop)       

        for i in self.viruses:

            try:
                new_virus.append(i.reproduce(self.popDensity))

            except NoChildException:
                continue

        # Merge two lists
        self.viruses = self.viruses + new_virus

        return self.getTotalPop()
#
# PROBLEM 2
#


def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """

    infection = []
    progression = []
    
    for i in range(0, 100):
        infection.append(SimpleVirus(0.1, 0.05))

    patient_zero = SimplePatient(infection, 1000)

    for i in range(0, 300):
        patient_zero.update()
        progression.append(len(patient_zero.viruses))
        pylab.plot(i, len(patient_zero.viruses), "b.")

        if len(patient_zero.viruses) <= 0:
            break

    pylab.title("Virus propagation")
    pylab.xlabel("Time")
    pylab.ylabel("Infection in body")
    pylab.show()


#
# PROBLEM 3
#
class ResistantVirus(SimpleVirus):
    """
    Representation of a virus which can have drug resistance.
    """    
    
    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):
        """
        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.
        
        maxBirthProb: Maximum reproduction probability (a float between 0-1)        
        
        clearProb: Maximum clearance probability (a float between 0-1).
        
        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.        
        """
        # TODO

        SimpleVirus.__init__(self, maxBirthProb, clearProb)
        self.resistances = resistances  # dict
        self.mutProb = mutProb  # float

    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        # TODO

        try:
            if self.resistances[drug] is True:
                return True

        except KeyError:
            # print "Key not found"
            return False

        return False

    def reproduce(self, popDensity, activeDrugs=None):
        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:       
        
        self.maxBirthProb * (1 - popDensity).                       
        
        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent). 

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.        

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90% 
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population        

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings). 
        
        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.         
        """
        # TODO

        # Look if drug is the patient system, and if so look if resistant

        for drugs in activeDrugs:
            if self.getResistance(drugs) is False:
                raise NoChildException()

        # reproduce
        if random.random() <= (self.maxBirthProb * (1 - popDensity)):  # Probability that the virus reproduce

            # mutation
            new_resis = self.resistances.copy()
            # new_resis = {}

            for i in self.resistances:

                if random.random() > (1 - self.mutProb):  # Children lost it

                    # Resistance hereditary
                    if self.resistances[i] is True: # Children lost it
                        new_resis[i] = False

                    # Switching resistance
                    elif self.resistances[i] is False:
                        new_resis[i] = True

            return ResistantVirus(self.maxBirthProb, self.clearProb, new_resis, self.mutProb)

        else:
            raise NoChildException()



class Patient(SimplePatient):
    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """
    
    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).               

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)
        
        maxPop: the  maximum virus population for this patient (an integer)
        """
        # TODO

        SimplePatient.__init__(self, viruses, maxPop)
        self.drugResist = []

    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        # TODO

        self.drugResist.append(newDrug)
        
        return self.drugResist

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        # TODO

        return self.drugResist

    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        # TODO

        count = 0

        for i in self.viruses:
            for y in drugResist:
                if i.getResistance(y) is True:
                    count += 1

        return count

    def update(self):
        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of 
          virus particles accordingly
          
        - The current population density is calculated. This population density
          value is used until the next call to update().

        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient. 
          The list of drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces. 

        returns: the total virus population at the end of the update (an
        integer)
        """
        # TODO

        new_virus = []

        # Clear viruses from list who died

        for i in self.viruses:
            if i.doesClear():
                self.viruses.remove(i)

            else:
                self.popDensity = self.getTotalPop() / float(self.maxPop)

                try:
                    new_virus.append(i.reproduce(self.popDensity, self.drugResist))

                except NoChildException:
                    continue

        self.viruses = self.viruses + new_virus

        return self.getTotalPop()


#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    # TODO

    infection = []
    progression = []
    
    for i in range(0, 100):
        infection.append(ResistantVirus(0.1, 0.05, {"guttagonol": False}, 0.005))

    patient_zero = Patient(infection, 1000)

    for y in range(0, 150):
        patient_zero.update()
        progression.append(len(patient_zero.viruses))
        pylab.plot(y, len(patient_zero.viruses), "b.")
        pylab.plot(y, patient_zero.getResistPop(["guttagonol"]), "g.")

    patient_zero.addPrescription("guttagonol")

    for z in range(150, 300):
        patient_zero.update()
        progression.append(len(patient_zero.viruses))
        pylab.plot(z, len(patient_zero.viruses), "r.")
        pylab.plot(z, patient_zero.getResistPop(["guttagonol"]), "g.")

    pylab.title("Virus propagation, guttagonol taken at 150")
    pylab.xlabel("Time")
    pylab.ylabel("Infection in body")
    pylab.show()

#
# PROBLEM 5
#


def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    # TODO

    answer = []
    count = 0

    num_of_trial = 300
    delay_of_drug = 75

    infection = []

    for i in range(0, 100):
        infection.append(ResistantVirus(0.1, 0.05, {"guttagonol": False}, 0.005))

    for sim in range(num_of_trial):
        temp_list = list(infection)
        a = run_sim_p5(delay_of_drug, Patient(temp_list, 1000))
        answer.append(a)
        if a < 50:
            count += 1

    print count, (count/len(answer))*100, "% of patient cured"

    pylab.title("Virus propagation, delayed treatment")
    pylab.hist(answer, bins=10)
    pylab.xlabel("Final total virus population")
    pylab.ylabel("number of patient")
    pylab.show()


def run_sim_p5(drug_timing, current_patient):
    '''Run a sim for a patient return final value of virus'''



    for y in range(1, drug_timing):
        current_patient.update()

    current_patient.addPrescription("guttagonol")

    for z in range(drug_timing + 1, drug_timing + 151):
        current_patient.update()

    answer = len(current_patient.viruses)

    return answer


#
# PROBLEM 6
#


def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    # TODO

    answer = []
    count = 0

    num_of_trial = 30
    delay_of_drug = 75

    infection = []

    for i in range(0, 100):
        infection.append(ResistantVirus(0.1, 0.05, {"guttagonol": False, "grimpex": False}, 0.005))

    for sim in range(num_of_trial):
        temp_list = list(infection)
        a = run_sim_p6(delay_of_drug, Patient(temp_list, 1000))
        answer.append(a)
        if a <= 50:
            count += 1


    pylab.title("Delay {}, {} trials, {} % of patient cured".format(delay_of_drug, num_of_trial, (count/len(answer))*100))
    pylab.hist(answer, bins=10)
    pylab.xlabel("Final total virus population")
    pylab.ylabel("number of patient")
    pylab.show()


def run_sim_p6(drug_timing, current_patient):
    '''Run a sim for a patient return final value of virus'''

    for y in range(0, 150):
        current_patient.update()

    current_patient.addPrescription("guttagonol")

    for z in range(0, drug_timing):
        current_patient.update()

    current_patient.addPrescription("grimpex")

    for x in range(0, 150):
        current_patient.update()

    answer = len(current_patient.viruses)

    return answer

#
# PROBLEM 7
#


def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    # TODO



    delay_of_drug = 150

    infection = []

    for i in range(0, 100):
        infection.append(ResistantVirus(0.1, 0.05, {"guttagonol": False}, 0.005))

    patient_1 = Patient(infection, 1000)
    patient_2 = Patient(infection, 1000)

    list_1 = run_sim_p8(delay_of_drug, patient_1)
    list_2 = run_sim_p8_2(delay_of_drug, patient_2)

    for data in list_1:
        pylab.plot(list_1.index(data), data, "b.")

    for data in list_2:
        pylab.plot(list_2.index(data), data, "r.")

    pylab.title("Virus propagation, problem 7")
    pylab.xlabel("Time")
    pylab.ylabel("Virus total")
    pylab.show()


def run_sim_p8(drug_timing, current_patient):
    '''Run a sim for a patient return final value of virus'''

    result = []

    for y in range(1, drug_timing):
        current_patient.update()
        result.append(current_patient.getTotalPop())

    current_patient.addPrescription("guttagonol")

    for z in range(0, 300):
        current_patient.update()
        result.append(current_patient.getTotalPop())

    current_patient.addPrescription("grimpex")

    for z in range(0, 150):
        current_patient.update()
        result.append(current_patient.getTotalPop())


    return result


def run_sim_p8_2(drug_timing, current_patient):
    '''Run a sim for a patient return final value of virus'''

    result = []

    for y in range(1, drug_timing):
        current_patient.update()
        result.append(current_patient.getTotalPop())

    current_patient.addPrescription("guttagonol")
    current_patient.addPrescription("grimpex")

    for z in range(0, 150):
        current_patient.update()
        result.append(current_patient.getTotalPop())

    return result


problem7()
