from midiutil import MIDIFile
import random as rand
# https://www.inspiredacoustics.com/en/MIDI_note_numbers_and_center_frequencies for notes

rand.seed(11293193898)

def build_file(notes):
    track    = 0
    channel  = 0
    time     = 0    # In beats
    duration = 0.5    # In beats
    tempo    = 240  # In BPM
    volume   = 100  # 0-127, as per the MIDI standard

    MyMIDI = MIDIFile(1)  # One track, defaults to format 1 (tempo track is created
                        # automatically)
    MyMIDI.addTempo(track, time, tempo)

    for i, pitch in enumerate(notes):
        MyMIDI.addNote(track, channel, pitch, time + i, duration, volume)

    with open("major-scale.mid", "wb") as output_file:
        MyMIDI.writeFile(output_file)

class MarkovNode:
    connections = []
    def __init__(self, note = 60):
        self.note = note

    def addConnection(self, otherNode, probability):
        if probability + self.sumOfProbabilities() > 1: return 1
        self.connections.append(MarkovConnection(self, probability, otherNode))
        return 0

    def sumOfProbabilities(self):
        sum = 0
        for connection in self.connections:
            sum += connection.probability
        return sum

    def gotoNextNode(self, randomObj):
        randomfloat = randomObj.random()
        sum = 0
        for connection in self.connections:
            sum += connection.probability
            if randomfloat < sum:
                return connection.other
            else: continue
        return self

class MarkovConnection:
    def __init__(self, first, probability, other):
        self.first = first
        self.probability = probability
        self.other = other

def build_chain_and_return_notes(randObject, notes, chance_to_connect, probability_scale, number_of_notes):

    nodes = []
    for note in notes:
        nodes.append(MarkovNode(note))
    
    randObject.shuffle(nodes)

    for node in nodes:
        nodesCopy = list(nodes)
        randObject.shuffle(nodesCopy)
        for node2 in nodesCopy:
            randomfloat = randObject.random()
            if randomfloat > chance_to_connect:
                probability = randObject.random() * probability_scale
                exitCode = node.addConnection(node2, probability)
                if exitCode == 1: break
    

    listOfNotes = []
    #startNodeIndex = randObject.randint(0, len(nodes) - 1)
    currentNode = nodes[0]
    for i in range(number_of_notes):
        listOfNotes.append(currentNode.note)
        currentNode = currentNode.gotoNextNode(randObject)
    return listOfNotes


rawNotes = [60, 62, 64, 65, 67, 69, 71]
#[64, 66, 67, 69, 71, 72, 74] #This is the E minor key. possibly add 76 for e5?

listOfNotesToPlay = build_chain_and_return_notes(rand, rawNotes, 0.4, 0.2, 20)


build_file(listOfNotesToPlay)