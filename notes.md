Table of Contents
-----------------

* [uNoGs](#unogs)
    * [Params](#params)
    * [Advanced Search Params](#advanced-search-params)
    * [Examples](#examples)
* [uNoGS NG](#unogs-ng)
    * [Examples](#examples-1)

uNoGs
-----

The unofficial Netflix online Global Search [API](https://rapidapi.com/unogs/api/unogs).

Base URLs:
* `https://unogs-unogs-v1.p.rapidapi.com/api.cgi`
* `https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi`

### Params

These are the (undocumented) params gathered from the various requests.

| param           | value(s)                                                                                   |
|-----------------|--------------------------------------------------------------------------------------------|
| t=\<type>       | ns, new, exp, genres, seasons, deleted, loadvideo, weeklynew, episodes, getimdb, imdb      |
| st=?            | 1,14,adv                                                                                   |
| sa=?            | and                                                                                        |
| ob=\<order-by>  | Relevance                                                                                  |
| p=\<page>       |                                                                                            |
| cl=\<country>   | US, all                                                                                    |
| q=\<query>      | get:\<qtype>:\<country>, {query} (qtype: get, new[days], exp, \<id>, {imdbid}, {filmid})   |

### Advanced Search Params

These are the alleged (according to the RapidAPI docs) fields for the advanced search.

| param               | description                         | value(s)                                                           |
|---------------------|-------------------------------------|--------------------------------------------------------------------|
| snfrate             | start netflix rating                | 0                                                                  |
| enfrate             | end netflix rating                  | 5                                                                  |
| simdbrate           | start imdb rating                   | 0                                                                  |
| eimdbrate           | end imdb rating                     | 10                                                                 |
| subtitle            | Subtitle Language                   | Any, English, Chinese                                              |
| sortby              | Sort By                             | Relevance, Date, Rating, Title, VideoType, FilmYear, Runtime       |
| syear               | Start Year                          | 1900                                                               |
| eyear               | End Year                            | 2020                                                               |
| audio               | Audio Type                          | Any, English, Chinese                                              |
| vtype               | Video Type                          | Any, Movie, Series                                                 |
| genreid             | Genre ID                            |                                                                    |
| page                | Page                                |                                                                    |
| clist               | Country List                        | all, 6, 78                                                         |
| query               | Query                               | new[days back], <any string>                                       |
| imdbvotes           | IMDB Votes                          | gt[num], lt[num]                                                   |
| andor               | Subtitle and/or Audio in language   | or (either in language), and (both in language)                    |
| downloadable        | Downloadable                        | Yes, No                                                            |

### Examples

| type                | request                                                                                                                                        |                                                               |
|---------------------|------------------------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------|
| genres              | api.cgi?t=genres                                                                                                                               |                                                               |
| new releases        | aaapi.cgi?q=get:new7:US&p=1&t=ns&st=adv                                                                                                        | aaapi.cgi?q=get%3Anew7%3AUS&p=1&t=ns&st=adv                   |
| expiring            | aaapi.cgi?q=get:exp:US&t=ns&st=adv&p=1                                                                                                         | aaapi.cgi?q=get%3Aexp%3AUS&t=ns&st=adv&p=1                    |
| deleted             | aaapi.cgi?t=deleted&cl=US&st=1                                                                                                                 |                                                               |
| deleted search      | aaapi.cgi?t=deleted&st=1&q={query}                                                                                                             |                                                               |
| load title details  | aaapi.cgi?t=loadvideo&q=60029591                                                                                                               |                                                               |
| update imdb         | aaapi.cgi/?t=imdb&q={imdbid}                                                                                                                   | aaapi.cgi/?t=imdb&q=%7Bimdbid%7D                              |
| load imdb           | aaapi.cgi?t=getimdb&q={filmid}                                                                                                                 |                                                               |
| weekly updates      | aaapi.cgi?t=weeklynew&cl=US,DE&q={query}&st=14                                                                                                 | aaapi.cgi?t=weeklynew&cl=US%252CDE&q=%7Bquery%7D&st=14        |
| advanced search     | aaapi.cgi?q=get%253Anew7-!1900,2018-!0,5-!0,10-!0-!Any-!Any-!Any-!gt100-!{downloadable%7D&t=ns&cl=all&st=adv&ob=Relevance&p=1&sa=and           |                                                               |


uNoGS NG
--------

Next Generation Netflix Global Search [API](https://rapidapi.com/unogs/api/unogsng).

Base URL: `https://unogsng.p.rapidapi.com`

### Examples

| type         | request                                                                                                                                                                    |
|--------------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| title detals | title?netflixid=81043135                                                                                                                                                   |
| expiring     | expiring?countrylist=78,46                                                                                                                                                 |
| search       | search?start_year=1972&orderby=rating&audiosubtitle_andor=and&limit=100&subtitle=english&countrylist=78,46&audio=english&country_andorunique=unique&offset=0&end_year=2019 |
| countries    | countries                                                                                                                                                                  |

### Search params

| field                        | description                             | value(s)                       |
|------------------------------|-----------------------------------------|--------------------------------|
| newdate=\<date>              | titles with new date grater than <date> | YYYY-MM-DD                     |
| genrelist=\<list>            | genre ids                               |                                |
| type=\<type>                 |                                         | movie, series                  |
| start_year=\<year>           |                                         | 4 digit year                   |
| end_year=\<year>             |                                         | 4 digit year                   |
| orderby=\<order>             |                                         | date,rating,title,type,runtime |
| audiosubtitle_andor=\<andor> |                                         | and, or                        |
| start_rating=\<rating>       | imdb rating                             | 0-10                           |
| end_rating=\<rating>         | imdb rating                             | 1-10                           |
| limit=\<limit>               |                                         | 1-100                          |
| subtitle=\<language>         | valid language string                   | english                        |
| audio=\<language>            | valid language string                   | english                        |
| countrylist=\<list>          | comma serperated list of country ids    | 78,46                          |
| query=\<title>               |                                         |                                |
| country_andorunique=\<v>     |                                         | unique                         |
| offset=\<num>                |                                         |                                |
