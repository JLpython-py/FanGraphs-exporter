<h1>FanGraphs-exporter</h1>

![GitHub repo size](https://img.shields.io/github/repo-size/JLpython-py/FanGraphs-exporter)
![GitHub last commit](https://img.shields.io/github/last-commit/JLpython-py/FanGraphs-exporter)
![GitHub](https://img.shields.io/github/license/JLpython-py/FanGraphs-exporter)

[FanGraphs](https://fangraphs.com) is an extremely expansive database of baseball statistics. Some of the pages, often the ones with the most number of available statistics, allow the user to configure the data which is outputted. The pages may also contain an **Export Data** button which allows the user to download the current data as a CSV file. FanGraphs-exporter attempts to automate the tasks of configuring the data and exporting it, allowing the user to export large quantities of data in a short period of time. The goal of this repository is to allow users to be able to export as much data from the FanGraphs website as possible.

<h1>Installation</h1>

[Download the latest release here](https://github.com/JLpython-py/FanGraphs-exporter/releases)

<h1>Requirements</h1>

- Python v3.6+
- geckodriver v0.29.0
- selenium v3.141.0

Install all requirements: `pip install -r requirements.txt`

<h1>Basic Usage</h1>

```python
import fgexporter

exporter = fgexporter.FanGraphs(setting="leaders")
exporter.export()
exporter.end_task()
```
