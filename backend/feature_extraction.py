import math
import re
from collections import Counter
from urllib.parse import urlparse
 
COMMON_TLDS = {
    "com", "org", "net", "edu", "gov", "mil", "int",
    "io", "co", "app", "dev", "info", "biz", "us", "uk",
    "ca", "de", "fr", "jp", "cn", "in", "au", "ru", "ch",
    "it", "nl", "se", "no", "es", "me", "tv", "xyz"
}
 
SUSPICIOUS_EXTENSIONS = (
    ".exe", ".zip", ".rar", ".scr", ".bat", ".cmd",
    ".apk", ".msi", ".jar", ".php", ".js", ".vbs"
)
 
 
def shannon_entropy(s):
    if not s:
        return 0.0
    counts = Counter(s)
    length = len(s)
    entropy = 0.0
    for count in counts.values():
        p = count / length
        entropy -= p * math.log2(p)
    return entropy
 
 
def get_netloc(url):
    working_url = url
    if "://" not in working_url:
        working_url = "http://" + working_url
    netloc = urlparse(working_url).netloc
    if "@" in netloc:
        netloc = netloc.split("@")[-1]
    if ":" in netloc:
        netloc = netloc.split(":")[0]
    return netloc
 
 
def normalize_url(url):
    if "://" not in url:
        return "https://" + url
    return url
 
 
def extract_features(url):
    url = normalize_url(url.strip())
    netloc = get_netloc(url)
 
    domain_parts = netloc.split(".")
    if len(domain_parts) >= 2:
        tld = domain_parts[-1]
        domain_name = domain_parts[-2]
    else:
        tld = ""
        domain_name = netloc
 
    subdomain_count = max(len(domain_parts) - 2, 0)
 
    url_length = len(url)
    num_dots = url.count(".")
    https_flag = 1 if url.lower().startswith("https") else 0
 
    tokens = re.split(r"[^a-zA-Z0-9]+", url)
    tokens = [t for t in tokens if t]
    token_count = len(tokens)
 
    num_digits = 0
    for char in url:
        if char.isdigit():
            num_digits += 1
 
    if url_length > 0:
        percentage_numeric_chars = (num_digits / url_length) * 100
    else:
        percentage_numeric_chars = 0.0
 
    has_hyphen_in_domain = 1 if "-" in netloc else 0
 
    tld_popularity = 1 if tld.lower() in COMMON_TLDS else 0
 
    path = urlparse(url if "://" in url else "http://" + url).path
    suspicious_file_extension = 1 if path.lower().endswith(SUSPICIOUS_EXTENSIONS) else 0
 
    features = {
        "url_length": url_length,
        "dot_count": num_dots,
        "https_flag": https_flag,
        "url_entropy": shannon_entropy(url),
        "token_count": token_count,
        "subdomain_count": subdomain_count,
        "tld_length": len(tld),
        "has_hyphen_in_domain": has_hyphen_in_domain,
        "number_of_digits": num_digits,
        "tld_popularity": tld_popularity,
        "suspicious_file_extension": suspicious_file_extension,
        "domain_name_length": len(domain_name),
        "percentage_numeric_chars": percentage_numeric_chars,
    }
 
    return features
 
 
def extract_features_batch(urls):
    rows = []
    for url in urls:
        rows.append(extract_features(url))
    return rows