# Example notebook

This is a simple example which illustrates how figures and text output can be
stripped.

```python
import numpy as np

x = np.linspace(0, 2.*np.pi, 1000)
y = np.sin(x)

print("The max of the data is {}".format(np.max(y)))
```

```python
%matplotlib inline
import matplotlib.pyplot as plt

plt.plot(x, y)
plt.xlabel("$x$")
plt.ylabel("$y = \sin{x}$")
```
