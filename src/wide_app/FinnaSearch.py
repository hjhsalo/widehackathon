# A function to make searchs from Finna
def FinnaSearch(searchwords, filters = [], limit = 10):
    res = []
    resultcount = 0
    for word in searchwords:
        result = finna.search(word,
                              #search_type=FinnaSearchType.Author,
                              fields=['title','nonPresenterAuthors','id','formats','subjects','year','languages','primaryAuthors'],
                              filters=filters, 
                              #sort=FinnaSortMethod.main_date_str_desc,
                              limit=limit)
        res.extend(result["records"])
        resultcount += result['resultCount']
    
    results = []
    for item in res:
        if item not in results:
            item['url'] = "https://www.finna.fi/Record/"+item['id']
            results.append(item)
    return results,resultcount
