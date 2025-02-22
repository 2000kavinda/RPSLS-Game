import cv2

def load_images():
    """
    Loads system hand images.
    """
    rock = cv2.imread('images/rock.png')
    paper = cv2.imread('images/paper.png')
    scissors = cv2.imread('images/scissors.png')

    rock = cv2.resize(rock, (200, 200))
    paper = cv2.resize(paper, (200, 200))
    scissors = cv2.resize(scissors, (200, 200))

    return {"Rock": rock, "Paper": paper, "Scissors": scissors}
