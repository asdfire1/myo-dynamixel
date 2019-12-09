
%%%% Units in m and kg %%%%

% Masses of links 
m1 = 0.225;
m2 = 0.213;
m3 = 0.227;

%symbolic variables
syms theta
syms o1    real %position
syms o2    real
syms o3    real
syms od1   real %angular velocity
syms od2   real
syms od3   real
syms od12  real %products of angular velocity 
syms od13  real
syms od23  real
syms od1sq real %squared values of angular velocities
syms od2sq real 
syms od3sq real
syms odd1  real %angulat accleration
syms odd2  real 
syms odd3  real
syms Grav real %symbolic value for gravity



%unit vectors in coordinate frames
xu = [1; 0;0];
zu = [0;0;1]; 

g = Grav*zu

% Local Inertia tensors

% moment of inertia for link1
I1xx =  0.00012925 ;  I1xy =  0.00000284 ;  I1xz = 0.00000121 ;
I1yx =  0.00000284  ;  I1yy =  0.00009182 ;  I1yz = 0.00000017 ;
I1zx = 0.00000121;  I1zy = 0.00000017 ;  I1zz =   0.00014905;

I1 = [I1xx I1xy I1xz;
      I1yx I1yy I1yz;
      I1zx I1zy I1zz];
  
  
% moment of inertia for link2
I2xx =  0.00068428;  I2xy = -0.00000062;  I2xz = -0.0003437 ;
I2yx = -0.00000062;  I2yy =  0.00070708;  I2yz =  0.0000108 ;
I2zx = -0.00003437;  I2zy =  0.0000108 ;  I2zz =  0.00005684;
I2 = [I2xx I2xy I2xz;
      I2yx I2yy I2yz;
      I2zx I2zy I2zz];
  
% moment of inertia for link1
I3xx =   0.00027740;  I3xy =  -0.00000012;  I3xz =  -0.00000966;
I3yx =  -0.00000012;  I3yy =   0.00034976;  I3yz =   0.00000191;
I3zx =  -0.00000966;  I3zy =   0.00000191;  I3zz =   0.00011907;

I3 = [I3xx I3xy I3xz;
      I3yx I3yy I3yz;
      I3zx I3zy I3zz];
  
% Link Lengths (end to end)  

L1 = 0.057*zu;
L2 = 0.22*xu;
L3 = 0.15*xu;

% Link Lengths (end to CoM)

Lc1 = 0.0285*zu;
Lc2 = 0.109*xu;
Lc3 = 0.075*xu;

% rotation marices

rotz(theta) = [cos(theta) -sin(theta) 0;
               sin(theta)  cos(theta) 0;
                        0           0 1];
roty(theta) = [cos(theta) 0 sin(theta);
                        0 1          0; 
              -sin(theta) 0 cos(theta)];
rotx(theta)=[1          0           0;
             0 cos(theta) -sin(theta);
             0 sin(theta)  cos(theta)];


R2 = rotz(o1)*rotx(deg2rad(-90))*rotz(o2);
R2 = vpa(R2,3);
R3 = rotz(o1)*rotx(deg2rad(-90))*rotz(o2+o3)
R3 = vpa(R3,3);

% Position Vectors (Local and Global frames)

S1  = L1;       %From base to frame 1
Sc1 = Lc1;
S2  = R2*L2;    %From frame 1 to frame 2
S2  = vpa(S2,3);
Sc2 = R2*Lc2;
Sc2 = vpa(Sc2,3);
S3  = R3*L3;    %From frame 2 to frame 3
S3  = vpa(S3,3);
Sc3 = R3*Lc3;
Sc3 = vpa(Sc3,3);

H1  = S1;       %From base to frame 1
Hc1 = Sc1;
H2  = H1+S2;    %From base to frame 2
Hc2 = H1+Sc2;
H3  = H2+S3;    %From base to frame 3
Hc3 = H2+Sc3;

% Angular Velocities

omega1 = od1*zu
omega2 = od2*[R2(1,3); R2(2,3); R2(3,3)]+omega1;
omega2 = vpa(omega2,3)
omega3 = od3*[R3(1,3); R3(2,3); R3(3,3)]+omega2;
omega3 = vpa(omega3,3)

% Transitional Velocities (end to end)

v1 = cross(omega1,S1);
v1 = vpa(v1,3)
v2 = v1 + cross(omega2,S2);
v2 = vpa(v2,3)
v3 = v2 + cross(omega3,S3);
v3 = vpa(v3,3)

% Transitional Velocities (end to CoM)

vc1 = cross(omega1,Sc1);
vc1 = vpa(vc1,3)
vc2 = v1 + cross(omega2,Sc2);
vc2 = vpa(vc2,3)
vc3 = v2 + cross(omega3,Sc3);
vc3 = vpa(vc3,3)

% Kinetic Energies

T1 = 1/2*m1*dot((vc1),vc1)+0.5*dot((I1*omega1),(omega1));
T1 = vpa(T1,3);
T2 = 1/2*m2*dot((vc2),vc2)+0.5*dot(((R2*I2*transpose(R2))*omega2),(omega2))       
T2 = vpa(T2,3);
T3 = 1/2*m3*dot((vc3),vc3)+0.5*dot(((R3*I3*transpose(R3))*omega3),(omega3))
T3 = vpa(T3,3);

% Potential Energies

V1 = m1*dot((g),Hc1)
V1 = vpa(V1,3);
V2 = m2*dot((g),Hc2)
V2 = vpa(V2,3);
V3 = m3*dot((g),Hc3)
V3 = vpa(V3,3);

% Langrange Equation

Lag = T1 - V1 + T2 - V2 + T3 - V3;
Lag = vpa(Lag,3);

dL_do1 = diff(Lag,od1);
dL_do1 = vpa(dL_do1,3)
dL_time1   = diff(dL_do1,o1)*od1+diff(dL_do1,o2)*od2+diff(dL_do1,o3)*od3+diff(dL_do1,od1)*odd1+diff(dL_do1,od2)*odd2+diff(dL_do1,od3)*odd3;
dL_time1   = vpa(dL_time1,3)
dL_o1  = diff(Lag,o1);
dL_o1  = vpa(dL_o1,3)
tau1       = vpa(simplify(dL_time1-dL_o1),3);

dL_do2 = diff(Lag,od2);
dL_do2 = vpa(dL_do2,3)
dL_time2   = diff(dL_do2,o1)*od1+diff(dL_do2,o2)*od2+diff(dL_do2,o3)*od3+diff(dL_do2,od1)*odd1+diff(dL_do2,od2)*odd2+diff(dL_do2,od3)*odd3;
dL_time2   = vpa(dL_time2,3)
dL_o2  = diff(Lag,o2);
dL_o2  = vpa(dL_o2,3)
tau2       = vpa(simplify(dL_time2-dL_o2),3);

dL_do3 = diff(Lag,od3);
dL_do3 = vpa(dL_do3,3)
dL_time3   = diff(dL_do3,o1)*od1+diff(dL_do3,o2)*od2+diff(dL_do3,o3)*od3+diff(dL_do3,od1)*odd1+diff(dL_do3,od2)*odd2+diff(dL_do3,od3)*odd3;
dL_time3   = vpa(dL_time3,3)
dL_o3  = diff(Lag,o3);
dL_o3  = vpa(dL_o3,3)
tau3       = vpa(simplify(dL_time3-dL_o3),3);



%% State space equation derivation

% Mass Matrix

M = [vpa(simplify(diff(tau1,odd1)),3) vpa(simplify(diff(tau1,odd2)),3) vpa(simplify(diff(tau1,odd3)),3);
     vpa(simplify(diff(tau2,odd1)),3) vpa(simplify(diff(tau2,odd2)),3) vpa(simplify(diff(tau2,odd3)),3);
     vpa(simplify(diff(tau3,odd1)),3) vpa(simplify(diff(tau3,odd2)),3) vpa(simplify(diff(tau3,odd3)),3)];

M = vpa(M,3)


% Accerleration function
 
QDD = [odd1;odd2;odd3];

% Coriolis coef?cients

tb1=subs(tau1,[od1*od2,od1*od3,od2*od3],[od12,od13,od23]);   % converts products of velocities into a funtion that is easily differentiable 
tb2=subs(tau2,[od1*od2,od1*od3,od2*od3],[od12,od13,od23]);
tb3=subs(tau3,[od1*od2,od1*od3,od2*od3],[od12,od13,od23]);


B = [vpa(simplify(diff(tb1,od12)),3) vpa(simplify(diff(tb1,od13)),3) vpa(simplify(diff(tb1,od23)),3);
     vpa(simplify(diff(tb2,od12)),3) vpa(simplify(diff(tb2,od13)),3) vpa(simplify(diff(tb2,od23)),3);
     vpa(simplify(diff(tb3,od12)),3) vpa(simplify(diff(tb3,od13)),3) vpa(simplify(diff(tb3,od23)),3)];

B = vpa(B,3);  

% Coriolis function

QD1 = [od1*od2;od1*od3;od2*od3];

% Centrifugal coefficeients

tc1=subs(tau1,[od1^2,od2^2,od3^2],[od1sq,od2sq,od3sq]);   % converts squared values of velocities into a funtion that is easily differentiable 
tc2=subs(tau2,[od1^2,od2^2,od3^2],[od1sq,od2sq,od3sq]);
tc3=subs(tau3,[od1^2,od2^2,od3^2],[od1sq,od2sq,od3sq]);

C = [vpa(simplify(diff(tc1,od1sq)),3) vpa(simplify(diff(tc1,od2sq)),3) vpa(simplify(diff(tc1,od3sq)),3);
     vpa(simplify(diff(tc2,od1sq)),3) vpa(simplify(diff(tc2,od2sq)),3) vpa(simplify(diff(tc2,od3sq)),3);
     vpa(simplify(diff(tc3,od1sq)),3) vpa(simplify(diff(tc3,od2sq)),3) vpa(simplify(diff(tc3,od3sq)),3)];
 
C = vpa(C,3);

% Centrifugal function

QD2 = [od1^2;od2^2;od3^2];

% Velocity terms

V = B*QD1 + C*QD2;

V = vpa(V,3);


% Gravity terms

G11  = [vpa(simplify(diff(tau1,Grav)),3);vpa(simplify(diff(tau2,Grav)),3);vpa(simplify(diff(tau3,Grav)),3)];
G12  = vpa(G11,3);
G12q = Grav*G12;
G = G12q;



%% Inverse Dynamics final equation

tau = M*QDD + V + G;
tau = vpa(tau,3)



%% Testing

%angularpositions 
pos1=0; pos2=-1; pos3=0.3;
%angularvelocities 
vel1=2; vel2=5; vel3=1;
%angularacceleration 
acc1=1; acc2=2; acc3=2;
%gConst=[0;0;9.81];
gFreeFall=9.81;
Tau_1=subs(tau(1,1),[o1,o2,o3,od1,od2,od3,odd1,odd2,odd3,Grav],[pos1,pos2,pos3,vel1,vel2,vel3,acc1,acc2,acc3,gFreeFall]); 
Tau_2=subs(tau(2,1),[o1,o2,o3,od1,od2,od3,odd1,odd2,odd3,Grav],[pos1,pos2,pos3,vel1,vel2,vel3,acc1,acc2,acc3,gFreeFall]); 
Tau_3=subs(tau(3,1),[o1,o2,o3,od1,od2,od3,odd1,odd2,odd3,Grav],[pos1,pos2,pos3,vel1,vel2,vel3,acc1,acc2,acc3,gFreeFall]);
Torq=[Tau_1;Tau_2;Tau_3];
Torq=vpa(Torq,3)
