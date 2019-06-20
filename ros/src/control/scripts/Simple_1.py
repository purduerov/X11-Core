"""
    Software's make-shift thrustmapping to try and circumvent some of the nuances of the
    Complex thrustmapping's implementation that exist without proper pool time to debug them
    out of the system

    [X, Y, Z, Roll, Pitch, Yaw] assumed
"""

import numpy as np
from pprint import pprint as pp

## The indexis of the thrusters
## Change this to configure the output
mappings = {
    "HFL": 0,
    "HFR": 1,
    "HBR": 2,
    "HBL": 3,
    "VFL": 4,
    "VFR": 5,
    "VBR": 6,
    "VBL": 7,
}

## The weights of each direction's influence
## Tweak these to scale the directional movement
weights = {
    "X": .40,
    "Y": .40,
    "Z": .30,
    "Roll": .125,
    "Pitch": .40,
    "Yaw": .20
}

## The thrusters associated with each direction, and their polarization 
##                              (front/back for positive direction value)
## Change these to influence what thrusters get influenced how by each direction
maskScaffolding = {
    "X": {"HFR": 1, "HFL": 1, "HBL": -1, "HBR": -1},
    "Y": {"HFR": 1, "HFL": -1, "HBL": -1, "HBR": 1},
    "Z": {"VFR": 1, "VFL": 1, "VBL": 1, "VBR": 1},
    "Roll": {"VFR": -1, "VFL": 1, "VBL": 1, "VBR": -1},
    "Pitch": {"VFR": -1, "VFL": -1, "VBL": 1, "VBR": 1},
    "Yaw": {"HFR": 1, "HFL": -1}
}

## This method returns a numpy array of the masks, in the order given from top down
## For the default order, top row is X's influences, second row is Y's influences, etc.
def getMasks(order=["X", "Y", "Z", "Roll", "Pitch", "Yaw"]):
    res = []

    for key in order:
        temp = [0] * 8

        for thrust in maskScaffolding[key]:
            temp[mappings[thrust]] = weights[key] * maskScaffolding[key][thrust]
            #print("temp[mappings[{}]] = weights[{}] * maskScaffolding[{}][{}]".format(thrust, key, key, thrust))

        res.append(temp)
        #print("{}:".format(key))
        #print(res[key])
    
    return np.asarray(res)

## Scales down the whole array to be under the given percentage (default, 80% thrust)
def scaleDown(arry, thresh=0.8):
    biggest = np.amax(arry)

    if biggest > thresh:
        pp("Scaled down!")
        pp(arry)
        scale = thresh / biggest
        arry = arry * scale
        pp(arry)
    
    return arry

## Runs the simple calculation to check what the combined output should be
def calculateSimple(desired, order=["X", "Y", "Z", "Roll", "Pitch", "Yaw"]):
    vecDict = {}
    vecMask = {}
    
    masks = getMasks(order=order)

    for i in range(len(desired)):
        key = order[i]
        vecDict[key] = desired[i]

        #print(key)
        #print(masks[i])

    ## Get the 8-vector controls from the masks against the 6-dof desired movement
    res = scaleDown(np.matmul(masks.transpose(), np.asarray(desired)), thresh=0.8)
    # print(res)

    return res

if __name__ == "__main__":
    for i in range(6):
        for j in range(6):
            a = [0] * 6
            a[i] = 1
            a[j] = 1
            calculateSimple(a)