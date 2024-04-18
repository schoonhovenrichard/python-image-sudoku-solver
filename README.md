# Python Susokdu solver from images

Solves a Sudoku based on a picture of it. Make sure the picture is exactly from the top without distortions, and black on white background.

# Installation
Requires tesseract to be installed.
```shell
sudo apt install tesseract-ocr
sudo apt install libtesseract-dev
```

The tesseract engine files can be downloaded:
```shell
wget https://github.com/tesseract-ocr/tessdata/raw/main/eng.traineddata
```

The data needs to be moved (something like one of these commands)
```shell
sudo mv -v eng.traineddata /usr/local/share/tessdata/
sudo mv -v eng.traineddata /usr/share/tesseract-ocr/4.00/tessdata/
```

Install Python packages:
```python
pip install -r requirements.txt
```

# Usage

```python
python main.py --image_path example_sudoku.jpg --m 3 --n 3
```
