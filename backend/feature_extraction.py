from urllib.parse import urlparse
 
 
def extract_features(url):
    url = url.strip()
 
    parsed_url = url
    if "://" not in url:
        parsed_url = "http://" + url
 
    parsed = urlparse(parsed_url)
    domain = parsed.netloc
    if "@" in domain:
        domain = domain.split("@")[-1]
    if ":" in domain:
        domain = domain.split(":")[0]
 
    domain_parts = domain.split(".")
    if len(domain_parts) >= 2:
        tld = domain_parts[-1]
    else:
        tld = ""
 
    num_subdomains = max(len(domain_parts) - 2, 0)
 
    url_length = len(url)
    domain_length = len(domain)
    tld_length = len(tld)
 
    num_dots = 0
    num_hyphens = 0
    num_digits = 0
    num_letters = 0
    num_special = 0
 
    for char in url:
        if char == ".":
            num_dots += 1
            num_special += 1
        elif char == "-":
            num_hyphens += 1
            num_special += 1
        elif char.isdigit():
            num_digits += 1
        elif char.isalpha():
            num_letters += 1
        elif not char.isalnum():
            num_special += 1
 
    if url_length > 0:
        letter_ratio = num_letters / url_length
        digit_ratio = num_digits / url_length
        special_ratio = num_special / url_length
    else:
        letter_ratio = 0.0
        digit_ratio = 0.0
        special_ratio = 0.0
 
    features = {
        "URLLength": url_length,
        "DomainLength": domain_length,
        "TLDLength": tld_length,
        "NumberOfSubdomains": num_subdomains,
        "NumberOfDots": num_dots,
        "NumberOfHyphens": num_hyphens,
        "NumberOfDigits": num_digits,
        "NumberOfLetters": num_letters,
        "SpecialCharacterCount": num_special,
        "LetterRatio": letter_ratio,
        "DigitRatio": digit_ratio,
        "SpecialCharacterRatio": special_ratio,
    }
 
    return features
 
 
def extract_features_batch(urls):
    rows = []
    for url in urls:
        rows.append(extract_features(url))
    return rows