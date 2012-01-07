#!/bin/sh

# pokrece se tako da je prvi parametar ime programa u trenutnom direktoriju
# drugi parametar ime izlaza (postavi .gs nastavak)

TRENUTNI=`pwd`
SRC=/media/data/DOCUMENTS/FER/5_SEMESTAR/PPJ/lab/src
L1=lab1_leksicka_analiza
L2=lab2_sintaksna_analiza

LEKSJED=$TRENUTNI/jedinke.out

cd $SRC
. ../venv/bin/activate

cd $SRC/$L1/analizator
python LA.py < $TRENUTNI/$1 > $LEKSJED 

cd $SRC/$L2/analizator
python SA.py < $LEKSJED > $TRENUTNI/$2

deactivate
cd $TRENUTNI
