import jpype
import jpype.imports
from jpype import *
import numpy as np
import graphviz
import command

# launch the JVM
# Start JVM with Java types on return

repobase = 'C:\\Users\\19527\\.m2\\repository'
fca = '.github/workflows/jar/ngs-fca-1.9-SNAPSHOT.jar'
bitset = '{}\\org\\dishevelled\\dsh-bitset\\3.0\\dsh-bitset-3.0.jar'.format(repobase)
functor = '{}\\org\\dishevelled\\dsh-functor\\1.0\\dsh-functor-1.0.jar'.format(repobase)
guava = '.github/workflows/jar/guava-31.0.1-jre.jar'
tinkerpop = '.github/workflows/jar/blueprints-core-2.6.0.jar'

jpype.startJVM(classpath=[fca, bitset, functor, guava, tinkerpop, 'classes'], convertStrings=False)

print('classpath: ')
print(java.lang.System.getProperty('java.class.path'))
print(java.lang.Long(10).longValue())

def bits(indexes):
    bits = JPackage('org').dishevelled.bitset.MutableBitSet()

    for index in indexes:
        bits.flip(index)

    return bits

lattice = JPackage('org').nmdp.ngs.fca.ConceptLattice(7)

lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([0]), bits([0, 1])))
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([1]), bits([0, 2])))
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([2]), bits([1, 2])));
#lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([3]), bits([0, 2, 4, 5])));
#lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([4]), bits([1, 3])));
#lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([5]), bits([0, 5])));

count = 0
for concept in lattice:
    count += 1

print("lattice size: {}".format(count))
print("lattice size: {}".format(lattice.size()))
print("lattice: {}".format(lattice.toString()))

f = open('lattice.dot', 'a')
f.write(str(lattice.toString()))
f.close()

g = graphviz.Source.from_file('lattice.dot')
g.view()

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.

if __name__ == '__main__':
    command.Command()
