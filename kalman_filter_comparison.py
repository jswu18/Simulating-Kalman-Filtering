import matplotlib.pyplot as plt 
import random
import math

x0 = 100 #initial position
r = 10 #noise
P_prior = [0]# a priori estimate of error
P_post = [0]# a posterior estimate of error
W = [0] #kalman gain
S = [0] # error in measurement
z_prior = [x0] # a priori estimate of measurement
z_meas_nk = [x0+random.uniform(-r, r)] # measurment for no kalman filter
z_meas_yk = [x0+random.uniform(-r, r)] # measurment for kalman filter
z_meas_zk = [x0] # measurment for no noise
x_prior_zk = [z_meas_zk[0]] #a priori state estimation for no kalman filter
x_prior_yk = [z_meas_yk[0]] #a priori state estimation for  kalman filter
x_prior_nk = [z_meas_nk[0]] #a priori state estimation for no noise
x_post_nk = [z_meas_nk[0]+random.uniform(-r, r)] #a posterior state estimation for no kalman filter
x_post_yk = [z_meas_yk[0]+random.uniform(-r, r)] #a posterior state estimation for kalman filter
x_post_zk = [z_meas_zk[0]] #a posterior state estimation for no noise
st_nk = [] #standard deviation list for no kalman filter
st_yk = [] #standard deviation list for kalman filter
k = 0.1 #proportional feedback gain
cov_vk = cov_wk = (1/3)*r*r #covariance of noise

#stepping through using kalman fitler
for i in range(1, 100):
 	uk = -k*(z_meas_yk[i-1])
 	vk = random.uniform(-r, r)
 	wk = random.uniform(-r, r)
 	x_prior_yk.append(x_post_yk[i-1] + uk)
 	z_prior.append(x_prior_yk[i])
 	z_meas_yk.append(z_prior[i] + wk)
 	P_prior.append(P_post[i-1]+cov_vk)
 	S.append(P_prior[i] + cov_wk)
 	if S[i] != 0:
 		W.append(P_prior[i]/S[i])
 	else:
 		W.append(0)
 	P_post.append(P_prior[i] - W[i]*W[i]*S[i])
 	x_post_yk.append(x_prior_yk[i]+W[i]*(z_prior[i]-z_meas_yk[i])+vk)
plt.plot(x_post_yk, label='Kalman Filter') #plotting 

#stepping through without kalman fitler and noise
for i in range(1, 100):
 	uk = -k*(z_meas_nk[i-1])
 	vk = random.uniform(-r, r)
 	wk = random.uniform(-r, r)
 	z_meas_nk.append(x_post_nk[i-1] + uk + wk)
 	x_post_nk.append(z_meas_nk[i]+vk)
plt.plot(x_post_nk, label='No Kalman Filter') #plotting

#stepping through without kalman fitler and no noise
for i in range(1, 100):
 	uk = -k*(z_meas_zk[i-1])
 	z_meas_zk.append(x_post_zk[i-1] + uk)
 	x_post_zk.append(z_meas_zk[i])
plt.plot(x_post_zk, label='Zero Noise (r = 0)') #plotting

#calculating standard deviation at each step with respect to no noise values
for i in range (1, 100):
	st_nk.append((x_post_nk[i]-x_post_zk[i])*(x_post_nk[i]-x_post_zk[i]))
	st_yk.append((x_post_yk[i]-x_post_zk[i])*(x_post_yk[i]-x_post_zk[i]))

#function to calculate the sum of a list (for standard deviation calculation)
def averagelist(inputlist):
    total = 0
    for i in range(len(inputlist)):
        total += inputlist[i]
    return total/len(inputlist)

#calculating and printing standard deviations
print("Comparison of Standard Devations of r = %f" %r)
print("Standard Deviation of No Kalman Filter %f" %math.sqrt(averagelist(st_nk)))
print("Standard Deviation of  Kalman Filter %f" %math.sqrt(averagelist(st_yk)))

#labelling graph
plt.legend(bbox_to_anchor=(0.75, 1), loc=2, borderaxespad=0.)
plt.ylabel('Position (State)')
plt.xlabel('Step')
plt.title('Kalman Filter Comparison(R = %f)' %r)
plt.show()