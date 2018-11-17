try:
    import httplib
except:
    import http.client as httplib


def have_internet():
    """Check if there is a internet connection

    Returns
    -------
    Boolean
        If there is a internet connection
    """
    conn = httplib.HTTPConnection("www.google.com", timeout=5)
    try:
        conn.request("HEAD", "/")
        conn.close()
        return True
    except:
        conn.close()
        print('Unable to connect to the internet')
        return False