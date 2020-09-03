import requests
from retrying import retry
from fake_useragent import UserAgent
from tqdm import tqdm
ua = UserAgent()


def _result(result):
    return result is None


@retry(stop_max_attempt_number=5, wait_fixed=2000, retry_on_result=_result)
def requests_get(url, headers=None, proxies=None):
    if headers is None:
        headers = dict()
    headers["user-agent"] = ua.random
    response = requests.get(url, headers=headers, timeout=3,
                            proxies={"http:": proxies, "https": proxies},
                            allow_redirects=False)
    return response


@retry(stop_max_attempt_number=5, wait_fixed=2000, retry_on_result=_result)
def requests_post(url, headers=None, data=None, proxies=None):
    if headers is None:
        headers = dict()
    headers["user-agent"] = ua.random
    response = requests.post(url, headers=headers, timeout=3, data=data,
                             proxies={"http:": proxies, "https": proxies},
                             allow_redirects=False)
    return response


def xstrip(source_str):
    """ 删除字符串中的多余空格、换行符等符号

    Args:
        source_str: 原始字符串

    Returns: 处理过后的字符串

    """
    import re
    return re.sub(r'\s+\r\n', ' ', source_str).strip()


def findall(re_pattern, source, first=True):
    """ 正则表达式查询

    Args:
        re_pattern: 正则表达式查询条件
        source: 网页源代码（文本）
        first: 是否取第一个

    Returns:
        提取的内容
    """
    import re
    match = re.findall(re_pattern, source, re.MULTILINE)
    if first:
        res = match[0] if match else ''
        res = xstrip(res)
    else:
        res = match if match else [None]
        res = [xstrip(x) for x in res]

    return res


def xpath(path_expression, source, first=True, child=False):
    """

    Args:
        path_expression: 查询条件，为 xpath 表达式
        source: 网页源代码 Element html
        first: 是否取第一个，如果是序列，则
        child: 是否包含子节点下的内容

    Returns:
        提取的内容
    """
    lxml_res = source.xpath(path_expression)
    if child:
        res = [xstrip(''.join(dd.itertext())) for dd in lxml_res]
        if res:
            return res[0]
    else:
        try:
            res = lxml_res
            if isinstance(res, list):
                if first:
                    res = xstrip(res[0]) if res else ''
                else:
                    res = [xstrip(x) for x in res]
            else:
                res = xstrip(res)
        except TypeError:
            print('ATTENTION: query condition is WRONG for child=False.')
            res = ''
        return res


class DownloadProgressBar(tqdm):
    def update_to(self, b=1, bsize=1, tsize=None):
        if tsize is not None:
            self.total = tsize
        self.update(b * bsize - self.n)


def download_file(url):
    import urllib.request
    file_name = url.split('/')[-1]
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc=url.split('/')[-1]) as t:
        urllib.request.urlretrieve(url, filename=file_name, reporthook=t.update_to)
