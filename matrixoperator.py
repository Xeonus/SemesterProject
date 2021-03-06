from Jama import Matrix as JMatrix
import Jama
from jarray import zeros, array
from java.lang import Class

# Copyright (c) Mark Longair 2010

# This is an example to show how you might wrap Jama's Matrix class
# for idiomatic use of matrix operations in Jython.  This is just a
# start to show what can be done.  Ideally you would wrap many more of the
# methods in Jama.Matrix, and also wrap the other Jama classes, namely:
#
#   CholeskyDecomposition
#   LUDecomposition
#   QRDecomposition
#   SingularValueDecomposition
#
# The documentation for Jama.Matrix is here:
#
#   http://math.nist.gov/javanumerics/jama/doc/Jama/Matrix.html
#
# Those methods that return basic types or void (e.g. det(), get(i,j),
# set(i,j)) can be used directly (i.e. without a wrapping method).

class EigenvalueDecomposition(object):

    def __init__( self, ed ):
        self.ed = ed

    def getRealEigenvalues( self ):
        return list( self.ed.getRealEigenvalues() )

    def getImagEigenvalues( self ):
        return list( self.ed.getRealEigenvalues() )

    def getV( self ):
        '''Return the eigenvector matrix'''
        return Matrix(self.ed.getV())

    def getD( self ):
        '''Return the block diagonal eigenvalue matrix'''
        return Matrix(self.ed.getD())

class Matrix(Jama.Matrix):

    def __init__( self, v ):
        '''Construct a matrix from an list of rows or an existing
        Jama.Matrix object'''
        if isinstance( v, Jama.Matrix ):
            m = v.getRowDimension()
            n = v.getColumnDimension()
            Jama.Matrix.__init__(self,m,n)
            self.setMatrix( 0, m-1, 0, n - 1, v )
            self.m, self.n = m, n
        else:
            ''' Assume it's an iterable object returning rows'''
            a = array( v, Class.forName("[D") )
            Jama.Matrix.__init__(self,a)
            self.m = self.getRowDimension()
            self.n = self.getColumnDimension()

    def getRow( self, row_index ):
        result = []
        for j in xrange(0,self.n):
            result.append(self.get(row_index,j))
        return result

    @staticmethod
    def random( m, n ):
        return Matrix(Jama.Matrix.random(m,n))

    def zeros( m, n ):
        return Matrix(Jama.Matrix(m, n))

    def inverse( self ):
        return Matrix(Jama.Matrix.inverse(self))

    def __str__( self ):
        result = "[ "
        for i in range(0,self.m):
            ss = [ str(x) for x in self.getRow(i) ]
            result += "\n  [ " + ', '.join(ss) + " ]"
        return result + "\n]"

    def __mul__( self, other ):
        return Matrix( self.times( other ) )

    def __add__( self, other ):
        return Matrix( self.plus( other ) )

    def __sub__( self, other ):
        return Matrix( self.minus( other ) )

    def __div__( self, other ):
        return Matrix( self.times ( 1 / other ) )

    def eig( self ):
        return EigenvalueDecomposition(Jama.Matrix.eig(self))

    def arraytimes( self, other):
        return Matrix( self.arrayTimes(other) )
        
    def dot( self, other):
        if self.getRowDimension() == other.getRowdimension():
 		result = 0
        if row_vector:
        	for i in xrange(0,sr):
        		result += self.get(0,i) * other.get(0,i)
        else:
        	for j in xrange(0,sc):
        		result += self.get(j,0) * other.get(j,0)

    def transpose( self ):
    	return Matrix( Jama.Matrix.transpose( self ) )

    def getColumn( self, column_index ):
        result = []
        for j in xrange(0,self.n):
            result.append(self.get(j,column_index))
        return result