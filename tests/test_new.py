from netflix.query import Page

def test_qtype():
    """test page.qtype"""
    page = Page("new", 1)
    assert page.qtype == "new1"

def test_expiring_url():
    """Ensure the full URL is as expected"""
    page = Page("new", 1)
    want = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi?q=get:new1:US&t=ns&st=adv&p=1"

    assert want == page.compiled_url
