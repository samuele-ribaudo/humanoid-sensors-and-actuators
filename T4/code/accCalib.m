% Compute the gain and the offset of the accelerometer
%
%   [M,w] = accCalib(acc)
%
%   acc: 3 x N matrix containing the acceleration measurements for the
%           calibration
%
%   M:  gain matrix, 3 x 3
%   w:  offset, 3 x 1
%   R:  rotation matrix (normalized matrix), 3 x 3
%   G:  gain matrix (diagonal matrix), 3 x 3
%
function [M,w,R,G] = accCalib(acc)

ax = acc(1,:);
ay = acc(2,:);
az = acc(3,:);

G = eye(3);
R = eye(3);

w = zeros(3,1);

%??????????????????????????????????????????????????????????????????????????
%   Implement the ellipsoid fitting algorthm which finally delivers w, R,
%   and G.

%   M is the model matrix and describes the transformation of the
%   uncalibrated acceleration measurement to the unit sphere. The
%   cooridnate system of the elliposid is not necessarily aligned to the
%   coordinate system of the accelerometer, i.e. R is usually not an
%   identiy matrix. R can later be used to transform the calibrated
%   measurements back to the coordinate system of the accelerometer.

% Transpose vectors to Nx1 column vectors for matrix operations
x = ax(:);
y = ay(:);
z = az(:);
N = length(x);

% Formulate the design matrix D and target vector O
D = [x.^2, y.^2, z.^2, x, y, z];
O = ones(N, 1);

% Solve the linear least-squares problem
v = D \ O;

% Extract algebraic coefficients
A_coeff = v(1);
B_coeff = v(2);
C_coeff = v(3);
G_coeff = v(4);
H_coeff = v(5);
I_coeff = v(6);

% Compute the offset Vector
w = [
    -G_coeff / (2 * A_coeff);
    -H_coeff / (2 * B_coeff);
    -I_coeff / (2 * C_coeff)
];

% Compute the scaling factor
kappa = 1 + (G_coeff^2 / (4 * A_coeff)) + (H_coeff^2 / (4 * B_coeff)) + (I_coeff^2 / (4 * C_coeff));

% Compute the diagonal gain matrix
G = diag([
    sqrt(kappa / A_coeff);
    sqrt(kappa / B_coeff);
    sqrt(kappa / C_coeff)
]);


% Rotation matrix
R = eye(3);
%??????????????????????????????????????????????????????????????????????????

M = G*R;

end