import cv2

# Load the Haar Cascade classifier for face detection
face_cascade = cv2.CascadeClassifier('path/to/haarcascade_frontalface_default.xml')

# Load the LBPH face recognition algorithm
face_recognizer = cv2.face.LBPHFaceRecognizer_create()

# Load the reference image containing the face you want to compare
reference_img = cv2.imread("path/to/reference/image.jpg", cv2.IMREAD_GRAYSCALE)

# Detect the face in the reference image
reference_faces = face_cascade.detectMultiScale(reference_img, scaleFactor=1.1, minNeighbors=5)

# Extract the face region from the reference image
for (x, y, w, h) in reference_faces:
    reference_face = reference_img[y:y+h, x:x+w]

# Extract the features from the reference face using LBPH
face_recognizer.train([reference_face], np.array([1]))

# Load the three other images you want to compare
test_img1 = cv2.imread("path/to/test/image1.jpg", cv2.IMREAD_GRAYSCALE)
test_img2 = cv2.imread("path/to/test/image2.jpg", cv2.IMREAD_GRAYSCALE)
test_img3 = cv2.imread("path/to/test/image3.jpg", cv2.IMREAD_GRAYSCALE)

# Detect the faces in the three other images
test_faces1 = face_cascade.detectMultiScale(test_img1, scaleFactor=1.1, minNeighbors=5)
test_faces2 = face_cascade.detectMultiScale(test_img2, scaleFactor=1.1, minNeighbors=5)
test_faces3 = face_cascade.detectMultiScale(test_img3, scaleFactor=1.1, minNeighbors=5)

# Extract the face regions from the three other images
for (x, y, w, h) in test_faces1:
    test_face1 = test_img1[y:y+h, x:x+w]
for (x, y, w, h) in test_faces2:
    test_face2 = test_img2[y:y+h, x:x+w]
for (x, y, w, h) in test_faces3:
    test_face3 = test_img3[y:y+h, x:x+w]

# Extract the features from the test faces using LBPH
_, test_label1 = face_recognizer.predict(test_face1)
_, test_label2 = face_recognizer.predict(test_face2)
_, test_label3 = face_recognizer.predict(test_face3)

# Compare the labels to determine if the faces match
if test_label1 == 1:
    print("Test image 1 contains a face matching the reference image")
else:
    print("Test image 1 does not contain a face matching the reference image")

if test_label2 == 1:
    print("Test image 2 contains a face matching the reference image")
else:
    print("Test image 2 does not contain a face matching the reference image")

if test_label3 == 1:
    print("Test image 3 contains a face matching the reference image")
else:
    print("Test image 3 does not contain a face matching the reference image")