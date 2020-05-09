# DictionaryCard
create card for vocabulary

## Installation
First install python
Then, 
```(bash)
git clone https://github.com/shyich03/DictionaryCard.git
python -m pip install --upgrade pip
python -m pip install --upgrade Pillow
cd DictionaryCard
```
add text.txt (the text file containing vocabularies) to the current directory
```(bash)
python app.py
```
retrieve images from the img folder

## text.txt format
Each vocab should consist of 4 lines
1. word name
2. description
3. example
4. a blank line

If a word have no explanation or example, put a blank line instead

Don't forget to add a blank line for the last word
