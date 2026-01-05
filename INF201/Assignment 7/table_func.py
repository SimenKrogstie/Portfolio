
import numpy as np

# y = x^2
def y(x):
	return x**2

# z = x^3
def z(x):
	return x**3

# w = x^4
def w(x):
	return x**4




x_values = np.arange(0, 20, 1)
y_values = y(x_values)
z_values = z(x_values)
w_values = w(x_values)


# make table
def print_table(x, y, z, w):
	# set s to the length of the longest number in x, y, z + a little extra space
	s = max(map(lambda arr: len(str(arr)), np.concatenate((x, y, z)))) + 3
	print(f"{'x':<{s}}|{'x^2':<{s}}|{'x^3':<{s}}|{'x^4':<{s}}")
	print(f"-"*(s*3+2))
	for i in range(len(x)):
		# aligned x to the left and y to the right
		print(f"{x[i]:<{s}}|{y[i]:<{s}}|{z[i]:<{s}}|{w[i]:<{s}}")

# Prints the output table
print_table(x_values, y_values, z_values, w_values)
