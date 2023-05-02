import jpype
import jpype.imports
from jpype import *
import numpy as np

# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.

# launch the JVM
# Start JVM with Java types on return

repobase = 'C:\\Users\\19527\\.m2\\repository'
fca = '{}\\org\\nmdp\\ngs\\ngs-fca\\1.9-SNAPSHOT\\ngs-fca-1.9-SNAPSHOT.jar'.format(repobase)
bitset = '{}\\org\\dishevelled\\dsh-bitset\\3.0\\dsh-bitset-3.0.jar'.format(repobase)
functor = '{}\\org\\dishevelled\\dsh-functor\\1.0\\dsh-functor-1.0.jar'.format(repobase)
guava = '{}\\com\\google\\guava\\guava\\31.0.1-jre\\guava-31.0.1-jre.jar'.format(repobase)
tinkerpop = '{}\\com\\tinkerpop\\blueprints\\blueprints-core\\2.6.0\\blueprints-core-2.6.0.jar'.format(repobase)

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

lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([0]), bits([0, 1, 3, 5])))
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([1]), bits([0, 1, 3, 4])))
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([2]), bits([0, 1, 3, 4, 5, 6])));
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([3]), bits([0, 2, 4, 5])));
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([4]), bits([1, 3])));
lattice.insert(JPackage('org').nmdp.ngs.fca.Concept(bits([5]), bits([0, 5])));

count = 0
for concept in lattice:
    count += 1

print("lattice size: {}".format(count))
print("lattice size: {}".format(lattice.size()))

def print_hi(name):
    # Use a breakpoint in the code line below to debug your script.
    print(f'Hi, {name}')  # Press Ctrl+F8 to toggle the breakpoint.


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
