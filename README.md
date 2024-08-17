# Generate list of words that share a common internal pattern

This program will, by default, generate a list of five letter words, grouped by words that share a common set of three internal characters. That is, the output will look something like:

```
=== acl ===
macle
vacla
=== aco ===
bacon
bacon
facom
jacob
jacob
lacon
macon
macon
pacos
racon
tacos
vacoa
yacov
=== acr ===
macri
macro
nacre
nacry
sacra
sacre
sacro
sacry
```

On my system, `/usr/share/dict/words` has around 500,000 words. Running this program takes just a few seconds to complete and produces just over 25,000 results.

## Getting started

1. Select the file [`wordmaker.py`](wordmaker.py), then click the "Download" link (![picture of download link](images/download-icon.png)). This will download the file `wordmaker.py` to your computer.

2. Open [Terminal.app](https://support.apple.com/guide/terminal/welcome/mac).

3. At the prompt, change to your `Downloads` directory:

    ```
    cd Downloads
    ```

4. Run the script using Python:

    ```
    python3 wordmaker.py -o words.txt
    ```

    This will output words to the file `words.txt`.

    **NB**: If this is the first time you are running the `python3` command, you will be prompted to install some software. Allow the software installation to complete, and then re-run the above command.

When the script completes, the file `words.txt` will contain the list of word groups.

## Advanced options

```
usage: wordmaker.py [-h] [--length LENGTH] [--word-list WORD_LIST]
                    [--output OUTPUT]

options:
  -h, --help            show this help message and exit
  --length, -l LENGTH   Extract words of this length
  --word-list, -w WORD_LIST
                        Path to word list
  --output, -o OUTPUT   Path to output file
```

For example, to produce words using an alternative word list:

```
python3 wordmaker.py -w my-list-of-words.txt -o words.txt
```

To produce a list of six-letter words (grouped by a common set of four characters):

```
python3 wordmaker.py -l 6 -o words.txt
```

## Alternative word lists

- The [Moby project](https://en.wikipedia.org/wiki/Moby_Project#Words) provides a number of potentially interesting word lists. You can find the list available for download on [Project Gutenberg](https://www.gutenberg.org/files/3201/files/).

- The [SCOWL (Spell Checker Oriented Word Lists) project](http://wordlist.aspell.net/) also provides a set of word lists.
