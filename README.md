# FanGraphs-exporter
FanGraphs is a well-known database among the baseball world filled with metrics concerning every aspect of baseball which you can imagine. These pages contain a large set of filters which allow the user to specify exactly what they are looking for. Often times, an **Export Data** is available which downloads the current data as a CSV file. 

FanGraphs-exporter automates these tasks, allowing the user to quickly specify the filters and download the data very quickly. Since not all of the pages contain the **Export Data** option, FanGraphs-exporter is being constantly updated so that, in the near future, users will also be able to export data without the option.

## Terminology
[FanGraphs homepage](https://fangraphs.com)

The term _Compatible Pages_ is used to describe web pages which can be exported using FanGraphs-exporter

Compatible Pages:
* Projections:
  * Pre-Season Projections
  * 600 PA/200 IP Projections
  * Updated In-Season Projections
  * 3 Year Projections
* Leaders:
  * Major League Leaders
  * KBO Leaders
  * Minor League Leaders
  * WAR Tools
* Prospects:
  * Prospects Home

## Projections
[FanGraphs Projections](https://fangraphs.com/projections.aspx)
### Configurations
Available Categories to Configure:
* Stats
* Position
* Team
* League
* Projection
* Update
### Basic Usage
```
import fgexporter
exporter = fgexporter.FanGraphs(setting="Projections")
exporter.name = "Sample Projection.csv"
exporter.config(Stats="Batting", Team="Dodgers")
exporter.export()
exporter.webdriver.quit()
```

## Leaders
[FanGraphs Leaderboards](https://fangraphs.com/leaders.aspx)
## Configurations
Available Categories to Configure:
* Group
* Stats
* League
* Team
* Split Teams
* Active Roster
* HOF
* Position
* Single Season
* Split
* Min
* Split Seasons
* Rookies
* Season 1, Season 2
* Age 1, Age 2
## Basic Usage
```
import fgexporter
exporter = fgexporter.FanGraphs(setting="Leaders")
exporter.name = "Sample Leader.csv"
exporter.config(Group="Team Stats", Position="SS", SingleSeason=2017)
exporter.export()
exporter.webdriver.quit()
```

## Prospects
[FanGraphs Leaderboards](https://fangraphs.com/prospects.aspx)
### Configurations
### Basic Usage
