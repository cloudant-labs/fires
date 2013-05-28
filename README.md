# FEMA Fires Project
This repo is a place holder for code around managing, analyzing and visualizing data from FEMA on national fires.

## Data Sources

* [RFP](http://hackforchange.org/challenge/fire-data-visualization)
* [Cleaned data](http://www.fema.gov/library/viewRecord.do?fromSearch=fromsearch&id=7443)

## Upload code
	
	python upload.py input_file.txt

where `inpute_file.txt` is assumed to have a specific structure (see gzipped version below).

## Target DB

Currently the target database is hard-coded to `fires2013`.  The username and password are pickd up automatically from a `~.clou` file.  There is sample data in [https://fema.cloudant.com/fires2013](https://fema.cloudant.com/fires2013).  See Mike Miller for credentials.