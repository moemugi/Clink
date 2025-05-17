from urllib.parse import urlparse, urlencode, unquote
import re
from datetime import datetime

def havingIP(url):
    ip_regex = r"\b(?:\d{1,3}\.){3}\d{1,3}\b"
    if re.search(ip_regex, url):
        return 1
    return 0

def haveAtSign(url):
    return 1 if "@" in url else 0

def getLength(url):
    return len(url)

def getDepth(url):
    path_segments = urlparse(url).path.split('/')
    return sum(1 for segment in path_segments if segment)

shortening_services = r"(bit\.ly|goo\.gl|shorte\.st|go2l\.ink|x\.co|ow\.ly|t\.co|tinyurl|tr\.im|is\.gd|cli\.gs|" \
                      r"yfrog\.com|migre\.me|ff\.im|tiny\.cc|url4\.eu|twit\.ac|su\.pr|twurl\.nl|snipurl\.com|" \
                      r"short\.to|BudURL\.com|ping\.fm|post\.ly|Just\.as|bkite\.com|snipr\.com|fic\.kr|loopt\.us|" \
                      r"doiop\.com|short\.ie|kl\.am|wp\.me|rubyurl\.com|om\.ly|to\.ly|bit\.do|lnkd\.in|db\.tt|" \
                      r"qr\.ae|adf\.ly|bitly\.com|cur\.lv|tinyurl\.com|ow\.ly|ity\.im|q\.gs|po\.st|bc\.vc|" \
                      r"twitthis\.com|u\.to|j\.mp|buzurl\.com|cutt\.us|u\.bb|yourls\.org|prettylinkpro\.com|" \
                      r"scrnch\.me|filoops\.info|vzturl\.com|qr\.net|1url\.com|tweez\.me|v\.gd|link\.zip\.net)"

def tinyURL(url):
    return 1 if re.search(shortening_services, url) else 0

def prefixSuffix(url):
    domain = urlparse(url).netloc
    return 1 if '-' in domain else 0

def no_of_dots(url):
    return url.count('.')

sensitive_words_list = [
    "account", "confirm", "banking", "secure", "ebyisapi", "webscr", "signin", "mail", "install", "toolbar",
    "backup", "paypal", "password", "username", "verify", "update", "login", "support", "billing", "transaction",
    "security", "payment", "online", "customer", "service", "accountupdate", "verification", "important",
    "confidential", "limited", "access", "securitycheck", "verifyaccount", "information", "change", "notice",
    "myaccount", "updateinfo", "loginsecure", "protect", "identity", "member", "personal", "actionrequired",
    "loginverify", "validate", "paymentupdate", "urgent", "porn", "suspend", "unsubscribe", "authorize",
    "click", "claim", "refund", "alert", "deactivation", "fraud", "recover", "reset", "charge", "webmail",
    "inbox", "lottery", "credit", "card", "debit", "bank", "ssn", "urgentaction", "restricted", "unlock",
    "warning", "temp", "hold", "accessaccount", "locked", "challenge", "securityupdate", "malware", "virus", "pornhub"
]

def sensitive_word(url):
    domain = urlparse(url).netloc
    return 1 if any(word in domain for word in sensitive_words_list) else 0

def has_unicode(url):
    parsed = urlparse(url)
    netloc = parsed.netloc
    try:
        decoded_netloc = netloc.encode('latin1').decode('idna')
    except:
        decoded_netloc = netloc
    unquoted_netloc = unquote(decoded_netloc)
    return 1 if unquoted_netloc != netloc else 0

def domainAge(domain_info):
    created = domain_info.creation_date
    expires = domain_info.expiration_date

    if not created or not expires:
        return 1

    if isinstance(created, list):
        created = created[0]
    if isinstance(expires, list):
        expires = expires[0]

    try:
        domain_lifetime = (expires - created).days
        return 1 if (domain_lifetime / 30) < 6 else 0
    except:
        return 1

def domainEnd(domain_info):
    expires = domain_info.expiration_date
    if isinstance(expires, str):
        try:
            expires = datetime.strptime(expires, "%Y-%m-%d")
        except:
            return 1
    if expires is None or isinstance(expires, list):
        return 1

    today = datetime.now()
    days_remaining = abs((expires - today).days)
    return 0 if (days_remaining / 30) < 6 else 1

def iframe(response):
    if response == "":
        return 1
    return 0 if re.findall(r"[<iframe>|<frameBorder>]", response.text) else 1

def mouseOver(response):
    if response == "":
        return 1
    try:
        return 1 if re.findall(r"<script>.+onmouseover.+</script>", response.text) else 0
    except:
        return 1

def forwarding(response):
    if response == "":
        return 1
    return 0 if len(response.history) <= 2 else 1
