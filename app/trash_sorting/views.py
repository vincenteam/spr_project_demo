import json
from collections import OrderedDict
import requests
from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from .models import SortSystem, Bin, Content, ContentType, Address

def current_datetime(request):
    return render(request, "page_1.html", {"test": "test value"})

def load_bins_data(bins_ids):
    bins_data = {}
    for b in [Bin.objects.get(id=id) for id in bins_ids]:
        bin_content = b.contents.all()
        bins_data[b] = {}
        for content in bin_content:
            if content.type not in bins_data[b].keys():
                bins_data[b][content.type] = [content]
            else:
                bins_data[b][content.type].append(content)

    return bins_data


def get_address_from_coords(lat:str, lon:str):
    url = "https://nominatim.openstreetmap.org/reverse?lat={}&lon={}&zoom=18&addressdetails=1&accept-language=en&format=json".format(lat, lon)
    res = requests.get(url)
    print(res.text)
    reverse_geocoded = json.loads(res.text, object_pairs_hook=OrderedDict)

    return reverse_geocoded["address"] if "address" in reverse_geocoded else None

def get_sort_system(address:OrderedDict):
    systems_addresses = {}

    for sys_address in Address.objects.all():
        system_id = sys_address.parent_system.id
        if system_id in systems_addresses:
            systems_addresses[system_id].append(json.loads(sys_address.address, object_pairs_hook=OrderedDict))
        else:
            systems_addresses[system_id] = [json.loads(sys_address.address, object_pairs_hook=OrderedDict)]

    #print("sys addrs ", systems_addresses)
    #print("req addr ", address)
    longest_match:(int, int) = None
    for sort_system_item in systems_addresses.items():
        for sys_address in sort_system_item[1]:
            match = True
            for field_item in reversed(sys_address.items()):
                if not field_item[0] in address or not address[field_item[0]] == field_item[1]:
                    match = False
                    break
            if match:
                match_len = len(sys_address)
                if longest_match is None or match_len > longest_match[1]:
                    longest_match = (sort_system_item[0], match_len)

    #print(longest_match)

    return longest_match[0] if longest_match is not None else None


@csrf_exempt
def test(request):
    if "lat" in request.POST and "lon" in request.POST:
        print(get_address_from_coords(request.POST["lat"], request.POST["lon"]))
    return HttpResponse("res")


def tmp():
    adresses =[
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10115", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10117", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10119", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10178", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10179", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10315", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10317", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10318", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10319", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10365", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10367", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10369", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10405", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10407", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10409", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10435", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10437", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10439", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10551", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10553", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10555", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10557", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10559", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10585", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10587", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10589", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10623", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10625", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10627", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10629", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10707", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10709", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10711", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10713", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10715", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10717", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10719", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10777", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10779", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10781", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10783", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10785", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10787", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10789", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10823", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10825", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10827", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "10829", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "11011", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12043", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12045", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12047", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12049", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12051", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12053", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12055", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12057", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12059", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12099", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12101", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12103", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12105", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12107", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12109", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12157", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12159", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12161", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12163", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12165", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12167", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12169", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12203", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12205", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12207", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12209", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12247", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12249", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12277", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12279", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12305", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12307", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12309", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12347", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12349", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12351", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12353", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12355", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12357", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12359", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12435", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12437", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12439", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12459", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12487", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12489", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12524", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12526", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12527", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12529", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12555", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12557", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12559", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12587", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12589", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12619", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12621", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12623", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12627", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12629", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12679", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12681", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12683", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12685", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12687", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "12689", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13051", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13053", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13055", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13057", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13059", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13086", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13088", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13089", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13125", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13127", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13129", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13156", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13158", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13159", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13187", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13189", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13347", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13349", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13351", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13353", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13355", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13357", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13359", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13403", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13405", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13407", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13409", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13435", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13437", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13439", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13465", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13467", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13469", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13503", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13505", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13507", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13509", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13581", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13583", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13585", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13587", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13589", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13591", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13593", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13595", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13597", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13599", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13627", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "13629", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14050", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14052", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14053", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14055", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14057", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14059", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14089", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14109", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14129", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14131", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14163", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14165", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14167", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14169", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14193", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14195", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14197", "country": "Germany", "country_code": "de"},
        {"city": "Berlin", "ISO3166-2-lvl4": "DE-BE", "postcode": "14199", "country": "Germany", "country_code": "de"},
    ]
    for a in adresses:
        ad = Address()
        ad.address = json.dumps(a)
        ad.parent_system = SortSystem.objects.get(name="Berlin")
        ad.save()

@csrf_exempt
def search(request):
    any_name = "any"
    choice_other = "other"
    search_session_variable = ["user_choices", "types_done_ids", "bins_ids"]
    new_search_session_var = "new_search"
    location_session_var = "location"
    lat_session_var = "lat"
    lon_session_var = "lon"

    new_search = False

    res = "res: "


    if new_search_session_var in request.POST:
        new_search = True
        for var in search_session_variable:
            request.session.pop(var, None)

        # replace with for loop in sessions_var
        request.session["user_choices"] = []
        request.session["types_done_ids"] = []


    #get location
    if lat_session_var in request.POST and lon_session_var in request.POST:
        lat = request.POST[lat_session_var]
        lon = request.POST[lon_session_var]
        request_addr = get_address_from_coords(lat, lon)

        if request_addr is None:
            res = "location lat:{}°, lon {}° does not exist in the database".format(lat, lon)
            return HttpResponse(res)

        sort_system_id = get_sort_system(request_addr)
        if sort_system_id is None:
            res = "location lat:{}°, lon {}° does not exist in the database".format(lat, lon)
            return HttpResponse(res)
        else:
            res += " {} \n".format(SortSystem.objects.filter(id=sort_system_id)[0].name)
            request.session[location_session_var] = sort_system_id
            print("new location")
    elif not location_session_var in request.session:
        res = "location is needed to make a research"
        return HttpResponse(res)


    #get bins ids
    sort_system = request.session[location_session_var]
    if not "bins_ids" in request.session:
        print("load bins from base")
        request.session["bins_ids"] = [b.id for b in  Bin.objects.filter(parent_system=sort_system)]
    bins_ids = request.session["bins_ids"]

    #get last user choice
    try:
        choice = request.POST["choice"]
    except KeyError:
        print("no user choice")
        choice = None
    request.session["user_choices"].append(choice)

    bins_data = load_bins_data(bins_ids)


    # modify bin list according to choice
    if choice and not new_search:
        print(bins_data.keys())

        for b_items in bins_data.items():
            content_found = False
            choice_type_id = request.session["types_done_ids"][-1]
            if choice_type_id in [t.id for t in b_items[1].keys()]:
                choice_type = next(t for t in b_items[1].keys() if t.id == choice_type_id)
                print("type in")
                names = [i.name for i in b_items[1][choice_type]]
                print(names, choice)
                if choice == choice_other:
                    if any_name in names:
                        content_found = True
                    else:
                        content_found = True
                        for ch in request.session["choices"]:
                            if ch in names:
                                content_found = False
                                break
                elif choice in names or any_name in names:
                    content_found = True
            else:
                if choice == choice_other:
                    content_found = True
            if not content_found:
                print("remove ", b_items[0].name, b_items[0].id)
                bins_ids.remove(b_items[0].id)

        request.session["bins_ids"] = bins_ids
        bins_data = load_bins_data(bins_ids)



    # create next question
    print(bins_data)
    types = {}
    for b in bins_data.values():
        for t in b.keys():
            if t.id not in request.session["types_done_ids"] and any_name not in [c.name for c in b[t]]:
                if t not in types.keys():
                    types[t] = len(b[t])
                else:
                    types[t] += len(b[t])

    print(types)

    def bin_priority(b):
        priority = 0
        for c_item in bins_data[b].items():
            if any_name in [c.name for c in c_item[1]]:
                priority += 1
        return priority

    # check for end condition
    if len(types) == 0:
        print("bin found")

        nb_fitting_bins = len(bins_data)
        if nb_fitting_bins == 0:
            print("no bin fit")
            bin_name = "no bin"
        elif nb_fitting_bins == 1:
            print("easy")
            bin_name = str(next(iter(bins_data)))
        else:
            print("multiple choices")
            bins_keys = list(bins_data.keys())
            list.sort(bins_keys, key=bin_priority)
            print(bins_keys)
            bin_name = str(bins_keys[0])
        res = "bin found: " + bin_name
        return render(request, "page_3.html", {"bin_name": bin_name})

    most_common_type = max(types, key=types.get)
    request.session["types_done_ids"].append(most_common_type.id)
    choices = []
    for b in bins_data.values():
        for item in b.items():
            if item[0].name == most_common_type.name:
                choices += item[1]
    choices = list(set(choices))

    print(most_common_type)
    print(choices)
    request.session["choices"] = [c.name for c in choices if c.name != any_name]
    request.session["choices"].append(choice_other)
    print(request.session["choices"])
    res += str(request.session["choices"])
    return render(request, "page_2.html", {"choice_type": most_common_type, "choices": request.session["choices"]})