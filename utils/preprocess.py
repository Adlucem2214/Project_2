# utils.py
import cv2
import face_recognition
import numpy as np

def align_face(image):
    face_landmarks_list = face_recognition.face_landmarks(image)
    if face_landmarks_list:
        # Get the landmarks of the first face
        landmarks = face_landmarks_list[0]
        left_eye = landmarks['left_eye']
        right_eye = landmarks['right_eye']

        # Compute the center of the eyes
        left_eye_center = np.mean(left_eye, axis=0).astype("int")
        right_eye_center = np.mean(right_eye, axis=0).astype("int")

        # Compute the angle between the eye centroids
        dY = right_eye_center[1] - left_eye_center[1]
        dX = right_eye_center[0] - left_eye_center[0]
        angle = np.degrees(np.arctan2(dY, dX))

        # Compute the desired right eye x-coordinate based on the desired
        # x-coordinate of the left eye
        desired_right_eye_x = 1.0 - 0.35

        # Determine the scale of the new resulting image by taking the ratio
        # of the distance between eyes in the current image to the ratio of
        # the distance between eyes in the desired image
        dist = np.sqrt((dX ** 2) + (dY ** 2))
        desired_dist = (desired_right_eye_x - 0.35)
        desired_dist *= 256
        scale = desired_dist / dist

        # Compute center (x, y)-coordinates (i.e., the median point) between
        # the two eyes in the input image
        eyes_center = (int((left_eye_center[0] + right_eye_center[0]) // 2),
                       int((left_eye_center[1] + right_eye_center[1]) // 2))

        # Grab the rotation matrix for rotating and scaling the face
        M = cv2.getRotationMatrix2D(eyes_center, angle, scale)

        # Update the translation component of the matrix
        tX = 256 * 0.5
        tY = 256 * 0.35
        M[0, 2] += (tX - eyes_center[0])
        M[1, 2] += (tY - eyes_center[1])

        # Apply the affine transformation
        (w, h) = (256, 256)
        output = cv2.warpAffine(image, M, (w, h), flags=cv2.INTER_CUBIC)

        return output
    return image

def preprocess_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image {image_path}")
        return None, None
    rgb_img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Align the face
    aligned_img = align_face(rgb_img)

    # Convert back to BGR for display
    aligned_bgr_img = cv2.cvtColor(aligned_img, cv2.COLOR_RGB2BGR)

    return aligned_bgr_img, aligned_img
