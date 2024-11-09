import cv2

# Open the default camera
cap = cv2.VideoCapture(1)

# Load the eye cascade classifier
eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

# Function to get the average color of a region
def get_average_color(frame, x, y, w, h):
    region = frame[y:y+h, x:x+w]
    avg_color_per_row = cv2.mean(region)
    return avg_color_per_row[:3]  # Return only BGR values

while True:
    # Capture frame-by-frame
    ret, frame = cap.read()
    if not ret:
        break

    # Convert the frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Apply histogram equalization
    gray = cv2.equalizeHist(gray)

    # Detect eyes in the frame with adjusted parameters
    eyes = eye_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=15, minSize=(30, 30))

    # Draw crosshairs at the center of the eyes and calculate cheek positions
    cheek_positions = []
    if len(eyes) >= 2:
        # Sort eyes by x-coordinate to identify left and right eyes
        eyes = sorted(eyes, key=lambda e: e[0])
        left_eye = eyes[0]
        right_eye = eyes[1]

        for (x, y, w, h) in [left_eye, right_eye]:
            center_x = x + w // 2
            center_y = y + h // 2
            # Draw horizontal line
            cv2.line(frame, (center_x - 10, center_y), (center_x + 10, center_y), (0, 255, 0), 2)
            # Draw vertical line
            cv2.line(frame, (center_x, center_y - 10), (center_x, center_y + 10), (0, 255, 0), 2)

        # Calculate cheek positions (assuming cheeks are below the eyes and further apart horizontally)
        cheek_x_left = left_eye[0] + left_eye[2] // 2 - int(0.5 * left_eye[2])
        cheek_x_right = right_eye[0] + right_eye[2] // 2 + int(0.5 * right_eye[2])
        cheek_y = left_eye[1] + int(1.5 * left_eye[3])
        cheek_positions.append((cheek_x_left, cheek_y))
        cheek_positions.append((cheek_x_right, cheek_y))

    # Draw crosshairs at the calculated cheek positions and get the color information
    for (cheek_x, cheek_y) in cheek_positions:
        # Draw horizontal line
        cv2.line(frame, (cheek_x - 10, cheek_y), (cheek_x + 10, cheek_y), (255, 0, 0), 2)
        # Draw vertical line
        cv2.line(frame, (cheek_x, cheek_y - 10), (cheek_x, cheek_y + 10), (255, 0, 0), 2)
        
        # Get the color information of the cheeks and display it
        cheek_color = get_average_color(frame, cheek_x - 10, cheek_y - 10, 20, 20)
        color_text = f'BGR: {int(cheek_color[0])}, {int(cheek_color[1])}, {int(cheek_color[2])}'
        cv2.putText(frame, color_text, (cheek_x + 15, cheek_y), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1, cv2.LINE_AA)

    # Display the resulting frame
    cv2.imshow('Camera', frame)

    # Press 'q' to exit
    if cv2.waitKey(1) == ord('q'):
        break

# When done, release the capture
cap.release()
cv2.destroyAllWindows()
