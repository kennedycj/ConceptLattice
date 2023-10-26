from jpype import JClass, JPackage

repobase = 'C:\\Users\\19527\\.m2\\repository'
fca = '.github/workflows/jar/ngs-fca-1.9-SNAPSHOT.jar'
bitset = '{}\\org\\dishevelled\\dsh-bitset\\3.0\\dsh-bitset-3.0.jar'.format(repobase)
functor = '{}\\org\\dishevelled\\dsh-functor\\1.0\\dsh-functor-1.0.jar'.format(repobase)
guava = '.github/workflows/jar/guava-31.0.1-jre.jar'
tinkerpop = '.github/workflows/jar/blueprints-core-2.6.0.jar'

def int(x):
    return JClass('java.lang.Integer')(x)
def date(year, month, day, hour=0, minute=0):
    return JClass('java.util.Date')(year - 1900, month - 1, day, hour, minute)

def interval(dimension, start, end):
    Range = JClass('com.google.common.collect.Range')
    return JPackage('org.nmdp.ngs.fca').Interval(dimension, Range.closed(start, end))
