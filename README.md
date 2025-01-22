Updated code for compatibility with Python 3.10
This work is based on the original implementation and documentation done by Juan Ruiz-Rosero, to whom the initial development credit belongs. As the versions of the graphical libraries (such as Matplotlib) and the Python environment have evolved, adjustments were made to ensure code compatibility with Python 3.10 and the latest versions of the dependencies.
The changes made are primarily technical and do not change the core functionality of the code. These updates include:
Syntax adjustments to accommodate Python 3.10.
Updated versions of graphical libraries, such as Matplotlib, to avoid conflicts and take advantage of performance and security improvements.
Minor code fixes to maintain compatibility with new versions of dependencies.
It should be noted that this project is open source, and the changes made respect the license and terms under which the original work is distributed. We thank Juan Ruiz-Rosero for his initial contribution, which has served as the basis for this update.
Note on the use of the code
Being an open source project, the community is invited to review, improve and contribute to the code, always respecting the original credits and license. The changes made in this update are available for use and distribution under the same terms.
# ScientoPy

ScientoPy is a open-source Python based scientometric analysis tool.
It has the following main characteristics: 

 
- Import Clarivate Web of Science (WoS) and Scopus data set
- Filter publications by document type
- Merge WoS and Scopus data set based on a field tags correlation table
- Find and remove duplicated documents
- H-index extraction for the analyzed topics.
- Country and institution extraction from author affiliations
- Top authors, countries, or institutions based on first document's authors or all document's authors
- Preprocessing brief graph and report table
- Top topics and specific topics analysis
- Wildcard topics search
- Trending topics using the top average growth rate (AGR)
- Five different visualization graphs: bar, bar trends, timeline, evolution, and word cloud
- Graphical user interface


Installation for Windows
========================

1. Download the latest stable release from: <https://github.com/jpruiz84/ScientoPy/releases>

2. Unzip the downloaded file and run ScientoPyGui.exe

For detailed instructions about ScientoPy Graphic User Interface, go to the user manual in 
[Manual/ScientoPyGui_user_manual.pdf](./Manual/ScientoPyGui_user_manual.pdf) 

Run ScientoPy for Ubuntu (or Debian based)
===========================================

To clone directly the last version from the repository run the following
git command:

    git clone https://github.com/jpruiz84/ScientoPy


Install prerequisites
----------------------

**IMPORTANT NOTE:** ScientoPy works with Python version 3.7 and not with version 3.11

1.  For run these commands to install Python3:

        sudo apt-get install python3.7 python3-tk python3-pip python3-pil python3-pil.imagetk
        
2.  Install the unidecode, numpy, scipy, matplotlib, and wordcloud
    Python libraries. For Windows, enter in the command line (Windows +
    R, cmd, and Enter), and run the installation script:

        python3 -m pip install --upgrade pip
        python3 -m pip install --user unidecode numpy pandas scipy matplotlib wordcloud
        

The bibliometric dataset
=======================

To download a custom dataset refer to the user manual: 
    [Manual/ScientoPy_user_manual.pdf](./Manual/ScientoPy_user_manual.pdf)
    
In this repo we include an example dataset that was donwloaded using: 
"Bluetooth low energy" as search criteria 


Running the ScientoPy Graphical User Interface GUI
==================================================

To run ScientoPy operations from the GUI, execute the following command:

    python3 scientoPyGui.py


Running the ScientoPy from console scripts
=========================================

This section describes the ScientoPy scripts to preprocess and analyze
the bibliometric dataset.

Preprocessing
-------------

First we need to preprocess the downloaded dataset. This preprocess
merge all the downloaded files from one folder to a single file. Also,
this process remove the duplicated files. To preprocess the example
dataset (“Internet of thing” AND “Gateway” located in dataInExample) run
this command inside ScientoPy folder:

    python3 preProcess.py dataInExample

Then, inside the folder `ScientoPy/dataPre` you will find the following
files:

-   **papersPreprocessed.tsv:** this file contains the information of
    all papers after the pre-process. This file will be used by the
    others scripts as the input data.

-   **PreprocessedBrief.tsv:** this file briefs the pre-process statics
    results, such as duplicated papers removed, types of documents, and
    others.

To find more options of the preprocessing script you can run:

    python3 preProcess.py -h

Extract the top topics
----------------------

With this script you can extract the top topics of a selected criterion.
The ScientoPy criterion are described bellow:


- **author:** Authors last name and first name initial
- **sourceTitle:** Publication or journal name
- **subject:** Research areas, only from WoS documents
- **authorKeywords:** Author keywords
- **indexKeywords:** Keywords generated by the index, from WoS Keyword
Plus, and from Scopus Indexed keywords
- **bothKeywords:** AuthorKeywords and indexKeywords are used for this
search
- **abstract:** Document abstract, for use with pre-defined topics and
asterisk wildcard
- **documentType:** Type of document
- **dataBase:** Database where the document was extracted (WoS or
Scopus)
- **country:** Country extracted from authors affiliations
- **institution:** Institution extracted from authors affiliations
- **institutionWithCountry:** Institution with country extracted from
authors affiliations

For example, to find the top author keywords you can run this script:

    python3 scientoPy.py -c authorKeywords

This will generate a list with the top 10 topics on the selected
criterion (in this case authorKeywords), with the number of documents
per topic, and the h-index associated to each one. Also, this script
graphs the evolution of each topic per year, and saves the quantitative
results on the folder `ScientoPy/results`.

This script have more options like, save the plot on a file, or increase
the number of topic results. For more information you can run:

    python3 scientoPy.py -h

Analyze custom topics inside a criterion
----------------------------------------

If you want to make an analysis of custom topics, such as the two
selected countries papers evolution, you can use the `scientoPy.py`
script, with the option `-t`, to specify the topics:

    python3 scientoPy.py -c country -t "United States; Brazil"

You can analyze any topic in any criterion. Put the topics on the `-t`
argument. Divide the topics with the `;`. Also, you can integrate two or
more topics in one, by dividing it with `,`. This is very useful for
abbreviations and plural singulars, for example:

    python3 scientoPy.py -c authorKeywords -t \
    "WSN, Wireless sensor network, Wireless sensor networks; RFID, RADIO FREQUENCY IDENTIFICATION"

**Note:** The command is very long, for that reason the command was
divided by `\`. If you have problems in Windows, remove the "" and put
the command in one single line.

### Asterisk (\*) wildcard

You can use the asterisk wildcard to find phrases or words which starts
or ends with the letters that you have inserted. For example, if you
want to find “device”, “devices”, and “device integration”, enter the
following command:

    python3 scientoPy.py -c authorKeywords -t "device*"

ScientoPy will print the topics found for the previous search:

    Topics found for device*:
    "devices;device management;Device Interactions;Device objectification;Device;Device integration"

You can use this information, to analyze each specific topic found, like
this:

    python3 scientoPy.py -c authorKeywords -t \
    "devices;device management;Device Interactions;Device objectification;Device;Device integration"

### Evolution plot

Also, you can see the results with a evolution graphic (add
`-g evolution`). This option plot the accumulative documents, average
documents per year (ADY), and PDLY, for example:

    python3 scientoPy.py -c authorKeywords -t \
    "WSN, Wireless sensor network, Wireless sensor networks; RFID, RADIO FREQUENCY IDENTIFICATION" \
    -g evolution

This script have more options like, save the plot on a file, or others.
For more information you can run:

    python3 scientoPy.py -h

Finding trending topics
-----------------------

This script finds the top trending topics based on the higher average
growth rate (AGR) over the others. The AGR is calculated on two years
periods. 

To find the top trending topics on author keywords criterion, you can
run the following script:

    python3 scientoPy.py -c authorKeywords --trend --startYear 2008 --endYear 2018 \
    --windowWidth 2  --agrForGraph -g evolution

This script will find the top 200 topics, then it calculates the AGR for
the last 2 years (`--windowWidth 2`). Finally, the 200 top topics are
sorted from the highest AGR in the last 2 year period to the lower. The
first 3 AGR topics are filtered (they correspond to the keyword Internet
of things), and the next 10 topics are garph in a evolution plot.

For more information about the AGR calculation refer to the 
PDF manual:


    Manual/ScientoPy_user_manual.pdf


Analysis based on the previous results
--------------------------------------

ScientoPy generates an output file with all the output documents from
the last run script. For example if we run the command:

    python3 scientoPy.py -c country -t "Canada" --noPlot

ScientoPy will create a documents output file
(`results/papersPreprocessed.tsv`) with all documents that have authors
with affiliation in Canada. This output file can be used by ScientoPy to
perform an analysis based on this, in that way if we run the following
command with the option `-r` or `--previousResults` after the previous
one to analyze based on the previous results:

    python3 scientoPy.py -c authorKeywords -r -g bar

we will obtain the top author keywords from papers where the author
affiliation correspond to Canada. Also, we can run the following command
to know which are the countries that have more common documents with
Canada:

    python3 scientoPy.py -c country -r -g bar

**Note:** the ScientoPy documents output file is only generated when the
`-r` or `--previousResults` is not used. In that way, if we run many
times a ScientoPy command with this option, the documents output file
will not overwritten.

Output files and directories
----------------------------

After run some ScientoPy commands or after run all the example commands
by executing the script `exampleGenerateGraphs.sh` you will find the
following folder and files structure described bellow:

-   **dataInExample:** contains Scopus and WoS example data set for the
    search criteria “Internet of things” AND “Gateway” downloaded in 27
    November 2017. This is the input example for preprocess script.

-   **dataPre:** output folder for the preprocess results, and input
    folder for scientoPy script.

    -   **papersPreprocessed.tsv:** preprocesed papers data with all input
        documents merged, filtered, and duplication removed. This is the
        input file that scientoPy script uses.
    
    -   **PreprocessedBrief.tsv:** preproceses brief table that shows the
        preprocess results related to total papers found per data base, the
        omitted papers, the duplicated papers count per data base, and the
        total number of papers per paper type (Conference paper, article,
        review...)

-   **graphs:** graphs output folder for preprocess and scientoPy
    scripts

-   **Manual:** folder with the pdf manual and example paper with
    scientoPy commands highlighted used for graph and tables generation.

-   **results:** output folder for scientoPy result output files

    -   **AuthorKeywords.tsv:** scientoPy output file for the selected
        criterion (in this case authorKeywords) that shows the top topics or
        the custom topics with the total number of documents, the Average
        Growth Rate (AGR), the Average Documents per Year (ADY), the
        h-index, and the documents per each year.
    
    -   **AuthorKeywords\_extended.tsv:** scientoPy output file for the
        selected criterion (in this case authorKeywords) that show the top
        or custom topics with the documents related to each one.
    
    -   **papersPreprocessed.tsv:** inside the results folder, this file
        contains the output papers from the last scientoPy used script. This
        is used as an input for scientoPy script when it use the option `-r`
        or `--previousResults`

ScientoPy graph types
=====================

ScientoPy has 5 different ways to graph the results described bellow:


| Graph type      | Argument        | Description                                                                                                                                       |
|-----------------|-----------------|---------------------------------------------------------------------------------------------------------------------------------------------------|
| Time line       | `-g time_line`     | Graphs the number of documents of each topic vs the publication year                                                                              |
| Horizontal bars | `-g bar`         | Graphs the total number of documents of each topic in horizontal bars                                                                             |
| Horizontal bars trends | `-g bar_trends`         | Graphs the total number of documents of each topic in horizontal bars, with the percentage of document published in the last years     |
| Word cloud      | `-g wordCloud`   | Generate a word cloud based on the topic total number of publications                                                                             |
| Evolution      | `-g evolution`  | Graphs two plots, one with the accumulative number of documents vs the publication year, and other with the average papers per year vs the percentage of documents in the last years |



To see graph examples refer to the PDF manual:

[Manual/ScientoPy_user_manual.pdf](./Manual/ScientoPy_user_manual.pdf)


## How to cite ScientoPy

If you use ScientoPy in a book, paper, website, technical report, etc., please include a reference to ScientoPy.

To cite ScientoPy, use the following [reference](https://link.springer.com/article/10.1007/s11192-019-03213-w):

> Ruiz-Rosero, J., Ramirez-Gonzalez, G., & Viveros-Delgado, J. (2019). Software survey: ScientoPy, a scientometric tool for topics trend analysis in scientific publications. Scientometrics, 1-24.

The bibtex entry for this is:

    @Article{Ruiz-Rosero2019,
        author="Ruiz-Rosero, Juan
        and Ramirez-Gonzalez, Gustavo
        and Viveros-Delgado, Jesus",
        title="Software survey: ScientoPy, a scientometric tool for topics trend analysis in scientific publications",
        journal="Scientometrics",
        year="2019",
        month="Nov",
        day="01",
        volume="121",
        number="2",
        pages="1165--1188",
        abstract="Bibliometric analysis is growing research filed supported in different tools. Some of these tools are based on network representation or thematic analysis. Despite years of tools development, still, there is the need to support merging information from different sources and enhancing longitudinal temporal analysis as part of trending topic evolution. We carried out a new scientometric open-source tool called ScientoPy and demonstrated it in a use case for the Internet of things topic. This tool contributes to merging problems from Scopus and Clarivate Web of Science sources, extracts and represents h-index for the analysis topic, and offers a set of possibilities for temporal analysis for authors, institutions, wildcards, and trending topics using four different visualizations options. This tool enables future bibliometric analysis in different emerging fields.",
        issn="1588-2861",
        doi="10.1007/s11192-019-03213-w",
        url="https://doi.org/10.1007/s11192-019-03213-w"
    }



## Authors

* **Juan Ruiz-Rosero** - *Initial work and documentation* 

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details


