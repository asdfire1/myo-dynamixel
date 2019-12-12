%% InverseKinrmatica
% 
% clear; %clear workspace
% clc; %clear screen
% close all; %close all figures



L_1 = 57 
L_2 = 219
L_3 = 147
% syms L_1 L_2 L_3
% syms theta1 theta2 theta3 theta11 theta22 theta33
theta1 = -90
theta2 = 0
theta3 = 90

%L   = Link( 'revolute', 'd', 1.2, 'a', 0.3, 'alpha', pi/2,          'modified');
L(1) = Link([ 0               L_1      0               0], 'modified');
L(2) = Link([ 0               0         0           -pi/2], 'modified');
L(3) = Link([ 0               0         L_2            0], 'modified');
L(4) = Link([ 0               0         L_3            0], 'modified');

CC04 = SerialLink([L(1) L(2) L(3) L(4)], 'name', 'CrustCrawler');
q=[theta1 theta2 theta3 0]*pi/180; 
T04 = CC04.fkine(q)



PP =  T04.t
P = [63.653; -110.250; 349.5]
Pxx = T04.t(1,:); 
Px = P(1,1)
Pyy = T04.t(2,:);
Py = P(2,1)
Pzz = T04.t(3,:);
Pz = P(3,1)
Pr = sqrt(Px^2+Py^2);
Ph = Pz - L_1;

% Inverse Kinematics for theta1

theta11 = atan2(Py,Px)
theta11=rad2deg(theta11)


% Inverse Kinematics for theta3

theta33a = acos((Pr^2+Ph^2-L_2^2-L_3^2)/(2*L_2*L_3))
theta33b = -acos((Pr^2+Ph^2-L_2^2-L_3^2)/(2*L_2*L_3))
theta33=rad2deg([theta33a theta33b])
% rad2deg(-theta33)

% Inverse Kinematics for theta2

Psi = acos((Pr^2+Ph^2+L_2^2-L_3^2)/(2*L_2*sqrt(Pr^2+Ph^2)))

beta = atan2(Ph,Pr)

theta22a=-(Psi+beta);
theta22a=rad2deg(theta22a)

theta22b=-(-Psi+beta);
theta22b= rad2deg(theta22b)

q1 = theta11

q2 = [theta22a theta22b]

q3 = theta33






































