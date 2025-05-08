import cv2

# Load and resize images for the game choices
def load_images():
    rock = cv2.imread('images/rock.png')
    paper = cv2.imread('images/paper.png')
    scissors = cv2.imread('images/scissors.png')
    lizard = cv2.imread('images/lizard.png')
    spock = cv2.imread('images/spock.png')

    rock = cv2.resize(rock, (200, 200))
    paper = cv2.resize(paper, (200, 200))
    scissors = cv2.resize(scissors, (200, 200))
    lizard = cv2.resize(lizard, (200, 200))
    spock = cv2.resize(spock, (200, 200))

    return {"Rock": rock, "Paper": paper, "Scissors": scissors,"Lizard": lizard,"Spock": spock}
