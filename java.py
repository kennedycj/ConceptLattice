from jpype import JClass, JPackage
from datetime import date

repobase = 'C:\\Users\\19527\\.m2\\repository'
fca = '.github/workflows/jar/ngs-fca-1.9-SNAPSHOT.jar'
bitset = '{}\\org\\dishevelled\\dsh-bitset\\3.0\\dsh-bitset-3.0.jar'.format(repobase)
functor = '{}\\org\\dishevelled\\dsh-functor\\1.0\\dsh-functor-1.0.jar'.format(repobase)
guava = '.github/workflows/jar/guava-31.0.1-jre.jar'
tinkerpop = '.github/workflows/jar/blueprints-core-2.6.0.jar'

def java_date(dt):
    return JClass('java.util.Date')(dt.year - 1900, dt.month - 1, dt.day)
def java_int(x):
    return JClass('java.lang.Integer')(x)

        #else raise exception

def python_date(jd):
    return date(jd.getYear() + 1900, jd.getMonth() + 1, jd.getDate())
def interval(start, end):
    Range = JClass('com.google.Concept.java.collect.Range')
    return JClass('org.nmdp.ngs.fca.Interval')(1, Range.open(start, end))
