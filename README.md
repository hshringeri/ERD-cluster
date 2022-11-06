# CS-473-Project-1
Steps to run Stage 1 of our Project:
1. Be sure to run 'pip install -r requirements.txt' to make sure all dependencies are included
    i. Pytesseract may need additonal instalation, see: https://github.com/UB-Mannheim/tesseract/wiki
2. Run 'python __main__.py' in the Stage_1 folder (or 'python .\Stage_1\'). The terminal will ask for a path to an image. The program will save a copy of the image with '-labeled' appended to the name in the same location. This image will be labeled with bounding boxes identifying each object within the ERD graph.
3. The terminal will output the list of ERD objects and their contents.