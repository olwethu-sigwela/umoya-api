from math import inf


def median(lst):

    if len(lst) == 1:
        return lst[0]

    sorted_lst = sorted(lst)

    n = len(sorted_lst)

    
    if n%2 != 0:
        return sorted_lst[n//2]
    else:
        return (sorted_lst[(n//2) - 1] + sorted_lst[((n//2)+1) - 1])/2

def price_per_mb(price, mb):
    return price/mb

def get_price_list(bundle_lst, currency = "ZAR"):
    
    return [bundle[f"Price ({currency})"] for bundle in bundle_lst]

def get_price_per_mb_list(bundle_lst, currency = "ZAR"):
    
    return [price_per_mb(bundle[f"Price ({currency})"], bundle["Size (MB)"]) for bundle in bundle_lst]

def get_cheapest_bundle(bundle_lst, currency="ZAR"):

    minimum_bundle_name = ""
    minimum_bundle_price = inf
    minimum_bundle_size = inf
    
    for bundle in bundle_lst:
        price = bundle[f"Price ({currency})"]
        if price < minimum_bundle_price:
            minimum_bundle_price = price
            minimum_bundle_name = bundle["Name"]
            minimum_bundle_size = bundle["Size (MB)"]

    
    return minimum_bundle_name, minimum_bundle_size, minimum_bundle_price

def get_carrier_names(data_dict):
    return [i for i in data_dict]

def get_price_per_mb_vs_size(data_dict, carrier, currency="ZAR"):
    
    prices = [i[f"Price ({currency})"] for i in data_dict[carrier][-1]["Data"]]
    sizes = [i[f"Size (MB)"] for i in data_dict[carrier][-1]["Data"]]
    prices_per_mb = [round(price_per_mb(p, s), 2) for p, s in zip(prices, sizes)]

    sizes = sizes
    prices_per_mb = prices_per_mb

    sizes, prices_per_mb = zip(*sorted(zip(sizes, prices_per_mb)))

    return sizes, prices_per_mb

def get_median_price_per_mb_vs_size(data_dict, carrier, currency="ZAR"):
    
    prices = [i[f"Price ({currency})"] for i in data_dict[carrier][-1]["Data"]]
    sizes = [i[f"Size (MB)"] for i in data_dict[carrier][-1]["Data"]]
    prices_per_mb = [price_per_mb(p, s) for p, s in zip(prices, sizes)]

    sizes = sizes
    prices_per_mb = prices_per_mb

    sizes, prices_per_mb = zip(*sorted(zip(sizes, prices_per_mb)))

    final_sizes = []
    final_prices_per_mb = []
    size_price_per_mb_dict = {}

    #This code makes sure that the sizes list only contains unique elements. Repeated sizes have their corresponding prices-per-mb replaced with their medians
    for i in range(len(sizes)): 
        if sizes[i] not in size_price_per_mb_dict:
            final_sizes.append(sizes[i])
            size_price_per_mb_dict[sizes[i]] = [prices_per_mb[i]]
        else:
            size_price_per_mb_dict[sizes[i]].append(prices_per_mb[i])

    for f_s in final_sizes:
        the_median = round(median(size_price_per_mb_dict[f_s]), 2)
        final_prices_per_mb.append(the_median)


    return final_sizes, final_prices_per_mb



    