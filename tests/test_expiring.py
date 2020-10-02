from netflix.query import Page

def test_qtype():
    page = Page("expiring", 1)
    assert page.qtype == "exp"

def test_expiring_url():
    """Ensure the full URL is as expected"""
    page = Page("expiring", 1)
    want = "https://unogs-unogs-v1.p.rapidapi.com/aaapi.cgi?q=get:exp:US&t=ns&st=adv&p=1"

    assert want == page.compiled_url
