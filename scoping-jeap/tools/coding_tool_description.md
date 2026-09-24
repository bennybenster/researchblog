---
title: "Extraction form tool"
description: "A browser based form for recording extraction data, written with the help of a Generative AI tool."
date: 2026-09-24
date-modified: 2026-09-24
---

The extraction form on the [main page](../index.html) describes what is recorded for each item and why. This page briefly describes the [html tool](./coding_tool.html) I used to support the extraction process.

## What it is 
I consulted Claude.ai (a generative AI tool) to help me develop a tool that uses html code to simplify the extraction process. It accepts a .csv file exported from Zotero, locally loads it (no data is sent anywhere), and allows it to be edited and saved. Items (journal articles) are shown one at a time with free-text fields to type in and dropdowns where appropriate. It will update the file every 20 seconds as a kind of autosave feature.

Essentially it is a tool for editing and saving a file that holds the data extracted for the analysis.

## Using it
Export a collection from Zotero as CSV. Open the tool, click **Open CSV...** and select the file. The tool maps Zotero's column names to its own, discards the columns it doesn't need and adds any extraction fields that are missing. 

Nothing is transmitted anywhere. The file is read and written locally through the browser and the page makes no network requests.

It is added here 'as is' as part of working towards a transparent process. Anyone could, if they wanted to develop something similar, download the html file and edit the field definitions to suit their own extraction project.

