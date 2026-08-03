from urllib.parse import urlparse

def feature_extraction(url):
    # Remove leading/trailing whitespace
    url = url.strip()

    # Add a default scheme if one is missing
    if not url.startswith(("http://", "https://")):
        url = "https://" + url

    parsed = urlparse(url)
    domain = parsed.netloc

    domain_labels = domain.split('.')
    tld = domain_labels[-1] if len(domain_labels) > 1 else ''
    num_subdomains = max(0, len(domain_labels) - 2)
    if num_subdomains < 0:
        num_subdomains = 0

    url_length = len(url)
    domain_length = len(domain)
    tld_length = len(tld)

    num_letters = 0
    num_digits = 0
    num_special = 0
    for char in url:
        if char.isalpha():
            num_letters += 1
        elif char.isdigit():
            num_digits += 1
        else:
            num_special += 1

    letter_ratio = num_letters / url_length if url_length > 0 else 0
    digit_ratio = num_digits / url_length if url_length > 0 else 0
    special_ratio = num_special / url_length if url_length > 0 else 0

    def char_class(c):
        if c.isalpha():
            return 'L'
        elif c.isdigit():
            return 'D'
        else:
            return 'S'

    same_class_count = 0
    for i in range(1, url_length):
        if char_class(url[i]) == char_class(url[i - 1]):
            same_class_count += 1
    char_continuation_rate = same_class_count / (url_length - 1) if url_length > 1 else 0

    features = {
        'URLLength': url_length,
        'DomainLength': domain_length,
        'TLDLength': tld_length,
        'NoOfSubDomain': num_subdomains,
        'CharContinuationRate': char_continuation_rate,
        'LetterRatioInURL': letter_ratio,
        'DegitRatioInURL': digit_ratio,
        'NoOfLettersInURL': num_letters,
        'NoOfDegitsInURL': num_digits,
        'SpacialCharRatioInURL': special_ratio
    }

    return features