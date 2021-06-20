This program is a prototype of an app.
The app has a goal to encourage people to read more books.

The app has 2 modes: the first one gives an opportunity to enter a film title and get a further information:
if the film is an adaptation of a book, the user receives the comparison of the film and books.
Otherwise the user receives books which are similar to the film.

The program works mainly with the genres and time of publication/release.
The books provided here are those which are connected to Lewis's Carroll's "Alice in Wonderland".
That is why the books recommendations and comparisons are limited by these books.

To use the program, download the csv and tsv files with film and books datasets,
rename the film datasets.
Download the British library dataset with the information about books following the link:
https://www.bl.uk/bibliographic/downloads/AlicesDayResearcherFormat_202006_csv.zip.
Then extract titles.csv from this archive to the folder where app_read.py is situated.
You will also need film datasets. Follow next links to download them:
1) title.basics.tsv - https://datasets.imdbws.com/title.basics.tsv.gz
2) title.crew.tsv - https://datasets.imdbws.com/title.crew.tsv.gz
3) title.principals.tsv - https://datasets.imdbws.com/title.principals.tsv.gz
4) name.basics.tsv -  https://datasets.imdbws.com/name.basics.tsv.gz
Each of these 4 files is an archive. You will need to extract the tsv file from them to the same folder where
app_read.py is situated. You will also need to rename them to 'title.basics.tsv', 'title.crew.tsv',
'title.principals.tsv' and 'name.basics.tsv' accordingly.

After that open app_read.py and start it. Then follow the instructions in terminal.
The result of them program are the book recommendations if it is run in the 2nd mode or if
the film chosen in the 1st mode is not a book adaptation.
If the program is run in the 1st mode and the chosen film is an adaptation of a book,
the result of the program is the comparison between the book and the film.