from netflix.query import Search
from py.path import local

def test_filepath():
    """Ensure that the Search.filepath is as expected"""
    search = Search("sin city")
    want = local(__file__).dirpath().join("..", "data/search/sin_city.json")
    assert want == search.filepath

def test_compiled_url():
    """Ensure that the request URL with params is as expected"""
    search = Search("sin city")
    want = "https://unogsng.p.rapidapi.com/search?type=movie&countrylist=78&audio=english&country_andorunique=unique&query=sin city"
    assert search.compiled_url == want
