import cv2
import numpy as np
import random

def solution(left_img, right_img):
    """
    :param left_img:
    :param right_img:
    :return: you need to return the result image which is stitched by left_img and right_img
    """
    # Calculating width and height for the output image.
    width = left_img.shape[1] + right_img.shape[1]
    height = left_img.shape[0]

    # Finding Key Points.
    sift = cv2.xfeatures2d.SIFT_create()
    kps_left, des_left = sift.detectAndCompute(left_img, None)
    kps_right, des_right = sift.detectAndCompute(right_img, None)

    # Finding the distances.
    matches = []
    distance = np.sqrt(np.sum((des_left[:, np.newaxis, :] - des_right[np.newaxis, :, :]) ** 2, axis=-1))
    for i, point in enumerate(kps_left):
        matches.append((kps_right[np.argmin(distance[i])], np.min(distance[i]), point))

    # Sorting the matches by distances and selecting the top 20.
    matches = np.array(matches)
    matches = matches[matches[:, 1].argsort()]
    matches = matches[:20]

    # Fining perspective transformation.
    p1 = np.array([np.array(match.pt) for match in matches[:, 2]])
    p2 = np.array([np.array(match.pt) for match in matches[:, 0]])
    homography, mask = cv2.findHomography(p2, p1, cv2.RANSAC, ransacReprojThreshold=3.0)

    # Stitching the images if the ratio of the matched keypoints is greater than 90%
    if (float(mask.sum()) / mask.size) > 0.9:
        result_image = cv2.warpPerspective(right_img, homography, (width, height))
        result_image[0:left_img.shape[0], 0:left_img.shape[1]] = left_img

        # To remove the blank pixels from the end of the result image.
        def crop(image):
            if not np.sum(image[:, -1]):
                return crop(image[:, :-2])
            return image

        return result_image
    else:
        return "Ratio of matched keypoints are not sufficient."


if __name__ == "__main__":
    left_img = cv2.imread('input/left.jpg')
    right_img = cv2.imread('input/right.jpg')
    result_image = solution(left_img, right_img)
    cv2.imwrite('results/stitched_result.jpg',result_image)


