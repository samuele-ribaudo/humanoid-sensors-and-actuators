import numpy as np
import quaternion
from ecompass import ecompass


def _todo(message):
    raise NotImplementedError(message)


def limit_vector_norm(v, max_norm):
    norm = np.linalg.norm(v)
    if norm > max_norm:
        return v * (max_norm / norm)
    return v


def stepImpl(obj, accelIn, gyroIn, magIn):
    # Fuse accelerometer, gyroscope, and magnetometer readings with an
    # indirect EKF.
    # accelIn - Nx3 matrix of accel samples in m/s^2
    # gyroIn - Nx3 matrix of gyro samples in rad/s
    # magIn - Nx3 matrix of normalized magnetometer samples

    accelIn = np.reshape(np.transpose(accelIn), (3, obj.DecimationFactor, -1))
    gyroIn = np.reshape(np.transpose(gyroIn), (3, obj.DecimationFactor, -1))
    magIn = np.reshape(np.transpose(magIn), (3, obj.DecimationFactor, -1))
    accelIn = np.transpose(accelIn, (1, 0, 2))
    gyroIn = np.transpose(gyroIn, (1, 0, 2))
    magIn = np.transpose(magIn, (1, 0, 2))
    ref = obj.ref_frame

    numiters = accelIn.shape[2]

    orientOut = obj.allocateOutputs(numiters)

    for iter in range(numiters):
        # The EKF state is the small error vector
        # [delta_theta, delta_b_g, delta_a_lin]. The nominal quaternion, gyro
        # bias, and linear acceleration are corrected after the update.

        omega_m = gyroIn[:, :, iter]

        a_m = accelIn[:, :, iter]
        m_m = magIn[:, :, iter]

        if obj.is_first_sample:
            # Basic tilt corrected ecompass orientation algorithm.
            # Do this the first time only. Need inputs, so not in setupImpl.

            obj.q_hat_plus = ecompass(a_m, m_m)
            obj.is_first_sample = False
        
        # Update the orientation quaternion based on the gyroscope readings.
        obj.q_hat_minus = obj.predictOrientation(omega_m, obj.b_g_hat, obj.q_hat_plus)

        # TODO EKF-3:
        # Use quaternion.as_rotation_matrix(obj.q_hat_minus) for this
        # conversion.
        R_q_hat_minus = _todo("TODO EKF-3: convert obj.q_hat_minus to a rotation matrix")

        z_a_hat_minus = obj.rotmat2gravity(R_q_hat_minus).T

        obj.a_lin_hat_minus = obj.LinearAccelerationDecayFactor * obj.a_lin_hat_plus
        z_a = ref.GravitySign * a_m + obj.a_lin_hat_minus
        # TODO EKF-4:
        # Build the accelerometer residual:
        # measured gravity estimate - gyro-predicted gravity estimate.
        r_a = _todo("TODO EKF-4: compute accelerometer residual")

        # TODO EKF-5:
        # Normalize m_m row-wise, predict the magnetic direction with
        # obj.rotmat2magnetic(R_q_hat_minus).reshape(1, 3), and subtract the
        # prediction from the normalized measurement.
        m_m_norm = _todo("TODO EKF-5: normalize the magnetometer measurement")
        m_s_hat_minus = _todo("TODO EKF-5: predict magnetic direction from R_q_hat_minus")
        r_m = _todo("TODO EKF-5: compute magnetometer residual")

        # TODO EKF-6:
        # Assemble the 6x9 observation matrix. The first three rows come from
        # gravity; the last three rows come from the magnetic field. Use
        # obj.buildHPart(...) for the -[v]_x blocks.
        H_a_theta = _todo("TODO EKF-6: gravity orientation-error block")
        H_a_bias = _todo("TODO EKF-6: gravity gyro-bias block")
        H_a = _todo("TODO EKF-6: concatenate accelerometer H blocks")
        H_m_theta = _todo("TODO EKF-6: magnetic orientation-error block")
        H_m_bias = _todo("TODO EKF-6: magnetic gyro-bias block")
        H_m = _todo("TODO EKF-6: concatenate magnetometer H blocks")
        H_k = _todo("TODO EKF-6: stack accelerometer and magnetometer H")

        # TODO EKF-7:
        # Stack the residual vector and build the 6x6 measurement covariance.
        r_k = _todo("TODO EKF-7: stack accelerometer and magnetometer residuals")
        R_k = _todo("TODO EKF-7: block-diagonal accel and magnetometer noise")
        P_minus = obj.P_minus

        # TODO EKF-8:
        # Compute innovation covariance S, Kalman gain K, and posterior
        # error-state estimate delta_x_hat.
        
        # -> R_k tells us how the errors from the sensors combined are (in sensor space!)
        # -> P_minus is kind of a probability, it tells us how likely the 9D error-state is
        # -> H_k is a remapping of P_minus in the sensor space
        # ---> S_k tells us the uncertainty
        S_k = H_k @ P_minus @ H_k.T + R_k

        # ---> K_k tells how strong the residuals should be corrected
        K_k = P_minus @ H_k.T @ np.linalg.inv(S_k)

        # ---> delta_x holds the vector (9 elements) that are needed for the correction
        # (0-3 for theta, 3-6 gyro bias, 6-9 accelerations)
        delta_x_hat = K_k @ r_k
        
        # Corrected error estimates
        delta_theta_hat = limit_vector_norm(delta_x_hat[0:3, 0], obj.MaxOrientationCorrection)
        delta_b_g_hat = limit_vector_norm(delta_x_hat[3:6, 0], obj.MaxGyroOffsetCorrection).reshape(1, 3)
        delta_a_lin_hat = delta_x_hat[6:, 0].reshape(1, 3)

        # TODO EKF-9:
        # Call quaternion.from_rotation_vector(-delta_theta_hat) to convert
        # orientation error into a correction quaternion, then right-multiply
        # it onto obj.q_hat_minus and normalize.
        delta_q = _todo("TODO EKF-9: convert orientation error to correction quaternion")
        obj.q_hat_plus = _todo("TODO EKF-9: apply orientation correction")
        obj.q_hat_plus /= np.linalg.norm(quaternion.as_float_array(obj.q_hat_plus))

        q_meas = ecompass(a_m, m_m)
        q_delta = obj.q_hat_plus.conjugate() * q_meas
        delta_theta_meas = limit_vector_norm(
            quaternion.as_rotation_vector(q_delta),
            obj.MaxOrientationCorrection,
        )
        delta_q_meas = quaternion.from_rotation_vector(obj.OrientationCorrectionGain * delta_theta_meas)
        obj.q_hat_plus = obj.q_hat_plus * delta_q_meas
        obj.q_hat_plus /= np.linalg.norm(quaternion.as_float_array(obj.q_hat_plus))
        
        # TODO EKF-10:
        # Under this residual convention, subtract the estimated vector errors
        # from the nominal gyro bias and linear acceleration.
        obj.b_g_hat = _todo("TODO EKF-10: correct gyro bias")
        obj.a_lin_hat_plus = _todo("TODO EKF-10: correct linear acceleration")

        # TODO EKF-11:
        # Compute posterior error covariance.
        P_plus = _todo("TODO EKF-11: compute posterior error covariance")
        P_minus_next = np.zeros((9, 9))

        diags_1_to_3 = np.arange(3)
        diags_4_to_6 = np.arange(3, 6)
        diags_7_to_9 = np.arange(6, 9)
        P_minus_next[diags_1_to_3, diags_1_to_3] = P_plus[diags_1_to_3, diags_1_to_3] + \
            (obj.dt**2) * (P_plus[diags_4_to_6, diags_4_to_6] + \
            (obj.GyroscopeDriftNoise + obj.GyroscopeNoise))

        P_minus_next[diags_4_to_6, diags_4_to_6] = P_plus[diags_4_to_6, diags_4_to_6] + obj.GyroscopeDriftNoise

        off_diag = -obj.dt * P_minus_next[diags_4_to_6, diags_4_to_6]
        P_minus_next[diags_4_to_6, diags_1_to_3] = off_diag
        P_minus_next[diags_1_to_3, diags_4_to_6] = off_diag

        
        P_minus_next[diags_7_to_9, diags_7_to_9] = (obj.LinearAccelerationDecayFactor**2) * \
            P_plus[diags_7_to_9, diags_7_to_9] + obj.LinearAccelerationNoise

        obj.P_minus = P_minus_next

        if obj.OrientationFormat.lower() == 'quaternion':
            orientOut[iter] = obj.q_hat_plus
        else:
            pass

    return orientOut
