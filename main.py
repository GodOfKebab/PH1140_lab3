from imutils.video import FPS
import imutils
import cv2


OPENCV_OBJECT_TRACKERS = {
    "csrt": cv2.TrackerCSRT_create,
    "kcf": cv2.TrackerKCF_create,
    "boosting": cv2.TrackerBoosting_create,
    "mil": cv2.TrackerMIL_create,
    "tld": cv2.TrackerTLD_create,
    "medianflow": cv2.TrackerMedianFlow_create,
    "mosse": cv2.TrackerMOSSE_create
}

tracker = OPENCV_OBJECT_TRACKERS["csrt"]()

initBB = None

vs = cv2.VideoCapture("27cm_smalltape.mov")

# initialize the FPS throughput estimator
fps = None

chose_object = False

position_x = list()
time_t = list()
t = 0

# loop over frames from the video stream
while t < 60.0:
    frame = vs.read()[1]

    # check to see if we have reached the end of the stream
    if frame is None:
        break

    # resize the frame (so we can process it faster) and grab the
    # frame dimensions
    frame = imutils.resize(frame, width=500)
    (H, W) = frame.shape[:2]

    # check to see if we are currently tracking an object
    if initBB is not None:
        # grab the new bounding box coordinates of the object
        (success, box) = tracker.update(frame)

        # check to see if the tracking was a success
        if success:
            (x, y, w, h) = [int(v) for v in box]
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            print("x( {}s ) = {}".format(str(round(t, 2)), (x + w / 2)))
            position_x.append((x + w / 2))
            time_t.append(round(t, 2))

        # update the FPS counter
        fps.update()
        fps.stop()

        # initialize the set of information we'll be displaying on
        # the frame
        info = [
            ("Success", "Yes" if success else "No"),
            ("FPS", "{:.2f}".format(fps.fps())),
        ]

        # loop over the info tuples and draw them on our frame
        for (i, (k, v)) in enumerate(info):
            text = "{}: {}".format(k, v)
            cv2.putText(frame, text, (10, H - ((i * 20) + 20)),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF
    t += 1 / 60.0

    # if the 's' key is selected, we are going to "select" a bounding
    # box to track
    if not chose_object:
        chose_object = True
        # select the bounding box of the object we want to track (make
        # sure you press ENTER or SPACE after selecting the ROI)
        initBB = cv2.selectROI("Frame", frame, fromCenter=False,
                               showCrosshair=True)

        # start OpenCV object tracker using the supplied bounding box
        # coordinates, then start the FPS throughput estimator as well
        tracker.init(frame, initBB)
        fps = FPS().start()

    # if the `q` key was pressed, break from the loop
    elif key == ord("q"):
        break

vs.release()

# close all windows
cv2.destroyAllWindows()

# print data collected
average = sum(position_x) / len(position_x)
for i in range(len(position_x)):
    position_x[i] -= average

dividing_factor = max(position_x)/0.2
for i in range(len(position_x)):
    position_x[i] /= dividing_factor

print("y =", position_x)
print("x =", time_t)
