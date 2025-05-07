# Purpose: Two-dimensional functions for interesting shapes
# Author:  Jarad Niemi
# Date:    2025-03-26

library("tidyverse")
library("mvtnorm")

# All functions will be on the unit square
d = expand.grid(
  x = seq(0, 1, length = 101),
  y = seq(0, 1, length = 101)
)

# Bivariate normal
bivariate_normal_function = function(x, y, mn = c(0, 0), sd = c(1, 1), rho = 0) {
  
  dmvnorm(cbind(x,y), mean = mn, 
          sigma = matrix(c(sd[1]^2, prod(sd)*rho, prod(sd)*rho, sd[2]^2),
                         nrow = 2))
}

d$bivariate_normal = bivariate_normal_function(d$x, d$y,
                                               mn  = c(0.5, 0.5),
                                               sd  = c(0.3, 0.3),
                                               rho = -0.9)

ggplot(d, 
       aes(x = x, y = y, fill = bivariate_normal)) +
  geom_tile()


# Banana distribution
# ideally this would have the reverse size as the logarithm
# but calculating that density will require computing a Jacobian
banana_function = function(x, y, a = 1.15, b = 0.5) {
  u1 = x/a
  u2 = a*(y-b*(x^2/a^2+a^2))
  
  bivariate_normal_function(u1, u2, rho = 0.9)
}

d$banana = banana_function(8*d$x - 4, 9*d$y - 2)

ggplot(d, 
       aes(x = x, y = y, fill = banana)) +
  geom_tile()



# Mixture of normals
# For the bottom of a rejection sampler
mixture <- function(x, y, p = 0.4, 
                    mu1 = rep(1/3, 2), mu2 = rep(2/3, 2), 
                    sd1 = rep(1/7, 2), sd2 = rep(1/7, 2), 
                    rho1 = 0, rho2 = 0) {
  (1 - p) * bivariate_normal_function(x, y, mu1, sd1, rho1) + 
       p  * bivariate_normal_function(x, y, mu2, sd2, rho2)
}

d$mixture = mixture(d$x, d$y)

ggplot(d, 
       aes(x = x, y = y, fill = mixture)) +
  geom_tile()

ggplot(d, 
       aes(x = x, y = y, z = mixture)) +
  geom_contour()
