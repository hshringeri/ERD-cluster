# CS-473-Project-1
## Created By: Youssuf Elshall, Lucas Baumgartner, Hardhi Shringeri, and Prajesh Sharma

### Prerequisites
1. Install tesseract using [the official installation instructions](https://tesseract-ocr.github.io/tessdoc/Installation.html).
2. Create a Python environment using `python3 -m venv env`.
3. Run a Python environment using `source env/bin/activate` for MacOS and Linux, or `.\env\Scripts\Activate.ps1` on Windows.
4. Install dependencies using `pip install -r requirements.txt`
5. You need to have an AWS account and have an [access key](https://docs.aws.amazon.com/general/latest/gr/aws-sec-cred-types.html#access-keys-about)

### Running the project
While in the project's root directory, you can run it using this command: `AWS_ACCESS_KEY_ID="YOUR_ACCESS_KEY" AWS_SECRET_ACCESS_KEY="YOUR_SECRET_KEY" python3 ./project/project.py`:

1. It will prompt you to choose a module to run.
2. Then, it will prompt for a path to an image or a path to `parameters.txt` relative to the project's root directory.

### Project structure
The folder `/project/` contains all of the required Python files for Stage 1 of the project:

`/project/`
- `project.py`: The main python file. The steps to execute are above.
- `colors.py`: A fun class that allows the printing of colored text to the terminal.
- `module_1.py`: Module that label an image using the trained tf model and returns the bounding boxes.
- `module_2.py`: Module that extracts text within the bounding boxes given by module 1.
- `module_3.py`: Module that processes text given by module 2.
- `module_4.py`: Module that clusters ERD images (converted to bag-of-words) given by `parameters.txt` using k-means++.
- `module_5.py`: Module that clusters ERD images (considering only their entities) given by `parameters.txt` using k-means++.

The folder `/Data/` contains all images used to train and test the models, as well as some useful python scripts.

### Format of `parameters.txt`
The first line is the path to the ERD images to cluster and the second line is the value of k. If k is 0, then the clustering modules will determine k based on the silhouette score.

Example `parameters.txt`:
```
./images/
3
```
