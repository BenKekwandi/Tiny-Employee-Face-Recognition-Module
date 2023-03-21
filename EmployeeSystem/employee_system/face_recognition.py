import cv2
import dlib

detector = dlib.get_frontal_face_detector()


predictor = dlib.shape_predictor("path/to/shape_predictor_68_face_landmarks.dat")
face_recognizer = dlib.face_recognition_model_v1("path/to/dlib_face_recognition_resnet_model_v1.dat")


reference_img = cv2.imread("path/to/reference/image.jpg")


reference_faces = detector(reference_img, 1)


reference_face_embedding = face_recognizer.compute_face_descriptor(reference_img, predictor(reference_faces[0]))


test_img1 = cv2.imread("path/to/test/image1.jpg")
test_img2 = cv2.imread("path/to/test/image2.jpg")
test_img3 = cv2.imread("path/to/test/image3.jpg")

test_faces1 = detector(test_img1, 1)
test_faces2 = detector(test_img2, 1)
test_faces3 = detector(test_img3, 1)

test_face_embedding1 = face_recognizer.compute_face_descriptor(test_img1, predictor(test_faces1[0]))
test_face_embedding2 = face_recognizer.compute_face_descriptor(test_img2, predictor(test_faces2[0]))
test_face_embedding3 = face_recognizer.compute_face_descriptor(test_img3, predictor(test_faces3[0]))

threshold = 0.6  
distance1 = dlib.distance(reference_face_embedding, test_face_embedding1)
distance2 = dlib.distance(reference_face_embedding, test_face_embedding2)
distance3 = dlib.distance(reference_face_embedding, test_face_embedding3)

if distance1 < threshold:
    print("Test image 1 contains a face matching the reference image")
else:
    print("Test image 1 does not contain a face matching the reference image")

if distance2 < threshold:
    print("Test image 2 contains a face matching the reference image")
else:
    print("Test image 2 does not contain a face matching the reference image")

if distance3 < threshold:
    print("Test image 3 contains a face matching the reference image")
else:
    print("Test image 3 does not contain a face matching the reference image")
