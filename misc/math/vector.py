from Numeric import *
from LinearAlgebra import *

def proj(M,x):
	# proj_w(x) = M(M^TM)^-1M^Tx
	return dot(dot(dot(M,inverse(dot(transpose(M),M))),transpose(M)),x)
def mat_array(s):
	return array([[int(v) for v in row.strip().split()] for row in [l for l in s.splitlines() if l]])
def col_array(s):
	return transpose(mat_array(s))
def norm(x):
	return sqrt(sum(x*x))
def unit(x):
	return x/norm(x)
def lss(A,b):
	"""Finds the least squares solution for Ax=b"""
	return dot(dot(inverse(dot(transpose(A),A)),transpose(A)),b)
